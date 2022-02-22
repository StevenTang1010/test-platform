#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:functions.py
@time:2022/01/05
@email:tao.xu2008@outlook.com
@description: 外部联系人回调事件处理
"""
from runner.customized.callback.external_contact import CallBackExternalContact


def call_back_add_external_contact(env_id, user_id, external_user_id):
    """
    添加企业客户事件
    :param env_id:
    :param user_id:
    :param external_user_id:
    :return:
    """
    ec = CallBackExternalContact(env_id)
    return ec.add_external_contact(user_id, external_user_id)


def call_back_edit_external_contact(env_id, user_id, external_user_id):
    """
    编辑企业客户事件
    :param env_id:
    :param user_id:
    :param external_user_id:
    :return:
    """
    ec = CallBackExternalContact(env_id)
    return ec.edit_external_contact(user_id, external_user_id)


def call_back_add_half_external_contact(env_id, user_id, external_user_id):
    """
    外部联系人免验证添加成员事件
    :param env_id:
    :param user_id:
    :param external_user_id:
    :return:
    """
    ec = CallBackExternalContact(env_id)
    return ec.add_half_external_contact(user_id, external_user_id)


def call_back_del_external_contact(env_id, user_id, external_user_id):
    """
    删除企业客户事件
    :param env_id:
    :param user_id:
    :param external_user_id:
    :return:
    """
    ec = CallBackExternalContact(env_id)
    return ec.del_external_contact(user_id, external_user_id)


def call_back_del_follow_user(env_id, user_id, external_user_id):
    """
    删除跟进成员事件
    :param env_id:
    :param user_id:
    :param external_user_id:
    :return:
    """
    ec = CallBackExternalContact(env_id)
    return ec.del_follow_user(user_id, external_user_id)


def call_back_transfer_fail(env_id, user_id, external_user_id):
    """
    客户接替失败事件
    :param env_id:
    :param user_id:
    :param external_user_id:
    :return:
    """
    ec = CallBackExternalContact(env_id)
    return ec.del_follow_user(user_id, external_user_id)


def call_back_create_chat(env_id, chat_id):
    """
    客户群创建事件
    :param env_id:
    :param chat_id:
    :return:
    """
    ec = CallBackExternalContact(env_id)
    return ec.create_chat(chat_id)


def call_back_update_chat(env_id, chat_id):
    """
    客户群变更事件
    :param env_id:
    :param chat_id:
    :return:
    """
    ec = CallBackExternalContact(env_id)
    return ec.update_chat(chat_id)


def call_back_dismiss_chat(env_id, chat_id):
    """
    客户群解散事件
    :param env_id:
    :param chat_id:
    :return:
    """
    ec = CallBackExternalContact(env_id)
    return ec.dismiss_chat(chat_id)


def call_back_create_tag(env_id, tag_id):
    """
    企业客户标签创建事件
    :param env_id:
    :param tag_id:
    :return:
    """
    ec = CallBackExternalContact(env_id)
    return ec.create_tag(tag_id)


def call_back_update_tag(env_id, tag_id):
    """
    企业客户标签变更事件
    :param env_id:
    :param tag_id:
    :return:
    """
    ec = CallBackExternalContact(env_id)
    return ec.update_tag(tag_id)


def call_back_delete_tag(env_id, tag_id):
    """
    企业客户标签删除事件
    :param env_id:
    :param tag_id:
    :return:
    """
    ec = CallBackExternalContact(env_id)
    return ec.delete_tag(tag_id)


if __name__ == '__main__':
    pass
