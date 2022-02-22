#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:utils.py
@time:2021/09/26
@email:tao.xu2008@outlook.com
@description:
"""
import os
import re
import shutil
import copy
import socket
import glob
import time
import json
import collections
import platform
import itertools
import uuid
from multiprocessing import Queue
from progressbar import ProgressBar, Percentage, Bar, RotatingMarker, ETA
from typing import Dict, List, Any

from pypinyin import lazy_pinyin
from loguru import logger
from runner import __version__
from runner.core import exceptions
from runner.core.models import VariablesMapping


def json_loads_str(content):
    try:
        return json.loads(content, strict=False)
    except json.JSONDecodeError as e:
        err_msg = "JSONDecodeError: JSON Content: {}\n{}".format(content, str(e))
        logger.error(err_msg)
        # return {}
        raise Exception(err_msg)


def json_dumps(d):
    return json.dumps(d, indent=2, ensure_ascii=False)


def to_safe_name(s):
    """
    替换字符串中非字母、数字、下划线的字符为下划线
    :param s: 原始字符串
    :return:
    """
    return str(re.sub("[^a-zA-Z0-9_]+", "", '_'.join(lazy_pinyin(s)))).lower()


def to_class_name(s):
    """
    中文转拼音，删除字符串中非字母、数字、下划线的字符，单词首字母大小，如："class-mall goods" --> ClassMallGoods
    :param s: 原始字符串
    :return:
    """
    if is_contains_chinese(s):
        s = '_'.join(lazy_pinyin(s)).title()
    if ' ' in s:
        s = s.title().replace(' ', '')
    return str(re.sub("[^a-zA-Z0-9]+", "", s))


def print_info(info_mapping):
    """
    print info in mapping.
        Args:
            info_mapping (dict): input(variables) or output mapping.
        Examples:
            >>> i_mapping = {
                    "var_a": "hello",
                    "var_b": "world"
                }
            >>> print_info(i_mapping)
            ==================== Output ====================
            Key              :  Value
            ---------------- :  ----------------------------
            var_a            :  hello
            var_b            :  world
            ------------------------------------------------
    """
    if not info_mapping:
        return

    content_format = "{:<16} : {:<}\n"
    content = "\n==================== Output ====================\n"
    content += content_format.format("Variable", "Value")
    content += content_format.format("-" * 16, "-" * 29)

    for key, value in info_mapping.items():
        if isinstance(value, (tuple, collections.deque)):
            continue
        elif isinstance(value, (dict, list)):
            value = json.dumps(value)
        elif value is None:
            value = "None"

        content += content_format.format(key, value)

    content += "-" * 48 + "\n"
    logger.info(content)


def get_platform():
    """获取测试平台版本信息"""
    return {
        "runner_version": __version__,
        "python_version": "{} {}".format(
            platform.python_implementation(), platform.python_version()
        ),
        "platform": platform.platform(),
    }


def get_local_ip():
    """
    Get the local ip address --linux/windows
    :return:(char) local_ip
    """
    return socket.gethostbyname(socket.gethostname())


def get_mac_address():
    """
    获取系统mac id
    ether 00:16:3e:17:7c:40  txqueuelen 1000  (Ethernet)
    ==> '00:16:3e:17:7c:40'
    :return:
    """
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])


def is_contains_chinese(string):
    """
    检查整个字符串是否包含中文
    :param string: 需要检查的字符串
    :return: bool
    """
    if string is None:
        string = ""
    if not isinstance(string, str):
        string = str(string)
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def select_chinese_one(str_list: list) -> str:
    """
    选择字符串列表中包含中文的字符串，如没有，返回第一个元素
    :param str_list:
    :return:
    """
    for string in str_list:
        if is_contains_chinese(string):
            return string
    else:
        return str_list[0]


def remove_files(base_dir, ext='test_*.py'):
    """
    使用通配符，获取文件并删除
    :return:
    """
    for f in glob.glob(os.path.join(base_dir, ext)):
        logger.info("remove {}".format(f))
        os.remove(f)


def rm_tree(base_dir, ext='test_*', max_rotation=0):
    """
    使用通配符，获取文件并删除
    :param base_dir:
    :param ext:
    :param max_rotation: 保留最大个数，0:不保留(按名字倒序排列后，删除列表尾部),
    如['test_01', 'test_02', 'test_03']，保留2个则删除test_01
    注意：文件夹名称排序，test3 > test11，所以最好数字补位成test_03<test_11
    :return:
    """
    targets = glob.glob(os.path.join(base_dir, ext))
    targets.sort(reverse=True)
    targets = targets[max_rotation:]

    for f in targets:
        if os.path.isdir(f):
            logger.info("remove tree dir {}".format(f))
            shutil.rmtree(f)
        elif os.path.isfile(f):
            logger.info("remove file {}".format(f))
            os.remove(f)
        else:
            logger.error("指定路径不存在！ - {}".format(f))


def zfill(number, width=6):
    """
    转换数字为字符串，并以’0‘填充左侧
    :param number:
    :param width: 最小宽度，如实际数字小于最小宽度，左侧填0
    :return: __zfill(123, 6) -> '000123'
    """
    return str(number).zfill(width)


def sleep_progressbar(seconds):
    """
    Print a progress bar, total value: seconds
    :param seconds:
    :return:
    """
    widgets = ['Progress: ', Percentage(), ' ', Bar(marker=RotatingMarker('-=>')), ' ', ETA()]
    pbar = ProgressBar(widgets=widgets, maxval=seconds).start()
    for i in range(seconds):
        pbar.update(1 * i + 1)
        time.sleep(1)
    pbar.finish()


def get_list_intersection(list_a, list_b):
    """
    Get the intersection between list_a and list_b
    :param list_a:
    :param list_b:
    :return:(list) list_intersection
    """

    assert isinstance(list_a, list)
    assert isinstance(list_b, list)
    return list((set(list_a).union(set(list_b))) ^ (set(list_a) ^ set(list_b)))


def set_os_environ(variables_mapping):
    """ set variables mapping to os.environ
    """
    for variable in variables_mapping:
        os.environ[variable] = variables_mapping[variable]
        logger.debug(f"Set OS environment variable: {variable}")


def unset_os_environ(variables_mapping):
    """ set variables mapping to os.environ
    """
    for variable in variables_mapping:
        os.environ.pop(variable)
        logger.debug(f"Unset OS environment variable: {variable}")


def get_os_environ(variable_name):
    """ get value of environment variable.

    Args:
        variable_name(str): variable name

    Returns:
        value of environment variable.

    Raises:
        exceptions.EnvNotFound: If environment variable not found.

    """
    try:
        return os.environ[variable_name]
    except KeyError:
        raise exceptions.EnvNotFound(variable_name)


def lower_dict_keys(origin_dict):
    """
    转换字典key为小写
    :param origin_dict:
    :return:
    Examples:
        >>> o_dict = {
            "Name": "",
            "URL": "",
        }
        >>> lower_dict_keys(o_dict)
            {
                "name": "",
                "url": "",
            }
    """
    if not origin_dict or not isinstance(origin_dict, dict):
        return origin_dict

    return {key.lower(): value for key, value in origin_dict.items()}


def omit_long_data(body, omit_len=512):
    """
    omit too long str/bytes  省略过长字符串
    :param body:
    :param omit_len:
    :return:
    """
    if not isinstance(body, (str, bytes)):
        return body

    body_len = len(body)
    if body_len <= omit_len:
        return body

    omitted_body = body[0:omit_len]

    appendix_str = f" ... OMITTED {body_len - omit_len} CHARACTORS ..."
    if isinstance(body, bytes):
        appendix_str = appendix_str.encode("utf-8")

    return omitted_body + appendix_str


# 生成笛卡尔积
def gen_cartesian_product(*args: List[Dict]) -> List[Dict]:
    """ generate cartesian product for lists

    Args:
        args (list of list): lists to be generated with cartesian product

    Returns:
        list: cartesian product in list

    Examples:

        >>> arg1 = [{"a": 1}, {"a": 2}]
        >>> arg2 = [{"x": 111, "y": 112}, {"x": 121, "y": 122}]
        >>> args = [arg1, arg2]
        >>> gen_cartesian_product(*args)
        >>> # same as below
        >>> gen_cartesian_product(arg1, arg2)
            [
                {'a': 1, 'x': 111, 'y': 112},
                {'a': 1, 'x': 121, 'y': 122},
                {'a': 2, 'x': 111, 'y': 112},
                {'a': 2, 'x': 121, 'y': 122}
            ]

    """
    if not args:
        return []
    elif len(args) == 1:
        return args[0]

    product_list = []
    for product_item_tuple in itertools.product(*args):
        product_item_dict = {}
        for item in product_item_tuple:
            product_item_dict.update(item)

        product_list.append(product_item_dict)

    return product_list


def merge_variables(
        variables: VariablesMapping, variables_to_be_overridden: VariablesMapping
) -> VariablesMapping:
    """ merge two variables mapping, the first variables have higher priority
    """
    step_new_variables = {}
    for key, value in variables.items():
        if f"${key}" == value or "${" + key + "}" == value:
            # e.g. {"base_url": "$base_url"}
            # or {"base_url": "${base_url}"}
            continue

        step_new_variables[key] = value

    merged_variables = copy.copy(variables_to_be_overridden)
    merged_variables.update(step_new_variables)
    return merged_variables


def sort_dict_by_custom_order(raw_dict: Dict, custom_order: List):
    def get_index_from_list(lst: List, item: Any):
        try:
            return lst.index(item)
        except ValueError:
            # item is not in lst
            return len(lst) + 1

    return dict(
        sorted(raw_dict.items(), key=lambda i: get_index_from_list(custom_order, i[0]))
    )


def is_support_multiprocessing() -> bool:
    try:
        Queue()
        return True
    except (ImportError, OSError):
        # system that does not support semaphores(dependency of multiprocessing), like Android termux
        return False


def seconds_to_hms(seconds: int) -> str:
    """
    秒数转时分秒
    :param seconds:
    :return:
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)


if __name__ == '__main__':
    pass
    # print(get_local_ip())
    # sleep_progressbar(3)
    # print(get_list_intersection([1, 2], [2, 3]))
    # print_info({"aaa": {"sd": 2}, "nbbb": 2})
    # print(get_platform())
    # print(to_safe_name("mall-goods搜索"))
    # print(to_class_name("mall-goods搜索"))
    # print(get_local_ip())
    # print(get_mac_address())
    # print(to_class_name("GetCustomerPool list A"))
    print(seconds_to_hms(300))
