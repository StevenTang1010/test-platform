#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:external_contact.py
@time:2021/08/16
@email:tao.xu2008@outlook.com
@description:
"""
import unittest
import time
from loguru import logger

from runner.customized.callback.base import CallBackRequest


class CallBackExternalContact(CallBackRequest):
    """客户联系回调"""
    def __init__(self, env_id, corp_id=None, token=None, aes_key=None, timestamp=None, nonce=None):
        super(CallBackExternalContact, self).__init__(env_id, corp_id, token, aes_key, timestamp, nonce)
        self.agent_id = self.env.data.get("login_agent_id")
        self.createtime = str(int(time.time()))
        base_url = self.env.config.get("base_url_mk").get("value")

        external_contact_path = "/wxwork/v1/callback/external_contact"
        self.url = "{}{}/{}".format(base_url, external_contact_path, self.corp_id)

    # 添加企业客户事件
    def add_external_contact(self, user_id, external_user_id):
        """
        添加企业客户事件: 配置了客户联系功能的成员添加外部联系人时，回调该事件
        :return:
        """
        template = """<xml>
        <ToUserName><![CDATA[%(toUser)s]]></ToUserName>
        <FromUserName><![CDATA[sys]]></FromUserName> 
        <CreateTime>%(CreateTime)s</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[change_external_contact]]></Event>
        <ChangeType><![CDATA[add_external_contact]]></ChangeType>
        <UserID><![CDATA[%(UserID)s]]></UserID>
        <ExternalUserID><![CDATA[%(ExternalUserID)s]]></ExternalUserID>
        <State><![CDATA[teststate]]></State>
        <WelcomeCode><![CDATA[WELCOMECODE]]></WelcomeCode>
        </xml>"""
        event_dict = {
            'toUser': self.corp_id,
            'CreateTime': self.createtime,
            'UserID': user_id,
            'ExternalUserID': external_user_id,
        }
        event_xml = template % event_dict
        return self.post_callback(self.url, event_xml, self.agent_id)

    # 编辑企业客户事件
    def edit_external_contact(self, user_id, external_user_id):
        """
        配置了客户联系功能的成员修改外部联系人的备注、手机号或标签时，回调该事件
        :return:
        """
        template = """<xml>
        <ToUserName><![CDATA[%(toUser)s]]></ToUserName>
        <FromUserName><![CDATA[sys]]></FromUserName> 
        <CreateTime>%(CreateTime)s</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[change_external_contact]]></Event>
        <ChangeType><![CDATA[edit_external_contact]]></ChangeType>
        <UserID><![CDATA[%(UserID)s]]></UserID>
        <ExternalUserID><![CDATA[%(ExternalUserID)s]]></ExternalUserID>
        </xml>"""
        event_dict = {
            'toUser': self.corp_id,
            'CreateTime': self.createtime,
            'UserID': user_id,
            'ExternalUserID': external_user_id,
        }
        event_xml = template % event_dict
        return self.post_callback(self.url, event_xml, self.agent_id)

    # 外部联系人免验证添加成员事件
    def add_half_external_contact(self, user_id, external_user_id):
        """
        外部联系人免验证添加成员事件：
        外部联系人添加了配置了客户联系功能且开启了免验证的成员时（此时成员尚未确认添加对方为好友），回调该事件
        :return:
        """
        template = """<xml>
        <ToUserName><![CDATA[%(toUser)s]]></ToUserName>
        <FromUserName><![CDATA[sys]]></FromUserName> 
        <CreateTime>%(CreateTime)s</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[change_external_contact]]></Event>
        <ChangeType><![CDATA[add_half_external_contact]]></ChangeType>
        <UserID><![CDATA[%(UserID)s]]></UserID>
        <ExternalUserID><![CDATA[%(ExternalUserID)s]]></ExternalUserID>
        <State><![CDATA[teststate]]></State>
        <WelcomeCode><![CDATA[WELCOMECODE]]></WelcomeCode>
        </xml>"""
        event_dict = {
            'toUser': self.corp_id,
            'CreateTime': self.createtime,
            'UserID': user_id,
            'ExternalUserID': external_user_id,
        }
        event_xml = template % event_dict
        return self.post_callback(self.url, event_xml, self.agent_id)

    # 删除企业客户事件
    def del_external_contact(self, user_id, external_user_id):
        """
        删除企业客户事件：配置了客户联系功能的成员删除外部联系人时，回调该事件
        :param user_id:
        :param external_user_id:
        :return:
        """
        template = """<xml>
        <ToUserName><![CDATA[%(toUser)s]]></ToUserName>
        <FromUserName><![CDATA[sys]]></FromUserName> 
        <CreateTime>%(CreateTime)s</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[change_external_contact]]></Event>
        <ChangeType><![CDATA[del_external_contact]]></ChangeType>
        <UserID><![CDATA[%(UserID)s]]></UserID>
        <ExternalUserID><![CDATA[%(ExternalUserID)s]]></ExternalUserID>
        </xml>"""
        event_dict = {
            'toUser': self.corp_id,
            'CreateTime': self.createtime,
            'UserID': user_id,
            'ExternalUserID': external_user_id,
        }
        event_xml = template % event_dict
        return self.post_callback(self.url, event_xml, self.agent_id)

    # 删除跟进成员事件
    def del_follow_user(self, user_id, external_user_id):
        """
        删除跟进成员事件：配置了客户联系功能的成员被外部联系人删除时，回调该事件
        :param user_id:
        :param external_user_id:
        :return:
        """
        template = """<xml>
        <ToUserName><![CDATA[%(toUser)s]]></ToUserName>
        <FromUserName><![CDATA[sys]]></FromUserName> 
        <CreateTime>%(CreateTime)s</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[change_external_contact]]></Event>
        <ChangeType><![CDATA[del_follow_user]]></ChangeType>
        <UserID><![CDATA[%(UserID)s]]></UserID>
        <ExternalUserID><![CDATA[%(ExternalUserID)s]]></ExternalUserID>
        </xml>"""
        event_dict = {
            'toUser': self.corp_id,
            'CreateTime': self.createtime,
            'UserID': user_id,
            'ExternalUserID': external_user_id,
        }
        event_xml = template % event_dict
        return self.post_callback(self.url, event_xml, self.agent_id)

    # 客户接替失败事件
    def transfer_fail(self, user_id, external_user_id):
        """
        客户接替失败事件：企业将客户分配给新的成员接替后，客户添加失败时回调该事件
        :param user_id:
        :param external_user_id:
        :return:
        """
        template = """<xml>
        <ToUserName><![CDATA[%(toUser)s]]></ToUserName>
        <FromUserName><![CDATA[sys]]></FromUserName> 
        <CreateTime>%(CreateTime)s</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[change_external_contact]]></Event>
        <ChangeType><![CDATA[transfer_fail]]></ChangeType>
        <FailReason><![CDATA[customer_refused]]></FailReason>
        <UserID><![CDATA[%(UserID)s]]></UserID>
        <ExternalUserID><![CDATA[%(ExternalUserID)s]]></ExternalUserID>
        </xml>"""
        event_dict = {
            'toUser': self.corp_id,
            'CreateTime': self.createtime,
            'UserID': user_id,
            'ExternalUserID': external_user_id,
        }
        event_xml = template % event_dict
        return self.post_callback(self.url, event_xml, self.agent_id)

    # 客户群创建事件
    def create_chat(self, chat_id):
        """
        客户群创建事件：有新增客户群时，回调该事件。收到该事件后，企业可以调用获取客户群详情接口获取客户群详情。
        :param chat_id:
        :return:
        """
        template = """<xml>
        <ToUserName><![CDATA[%(toUser)s]]></ToUserName>
        <FromUserName><![CDATA[sys]]></FromUserName> 
        <CreateTime>%(CreateTime)s</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[change_external_chat]]></Event>
        <ChatId><![CDATA[%(ChatId)s]]></ChatId>
        <ChangeType><![CDATA[create]]></ChangeType>
        </xml>"""
        event_dict = {
            'toUser': self.corp_id,
            'CreateTime': self.createtime,
            'ChatId': chat_id
        }
        event_xml = template % event_dict
        return self.post_callback(self.url, event_xml, self.agent_id)

    # 客户群变更事件
    def update_chat(self, chat_id):
        """
        客户群变更事件：客户群被修改后（群名变更，群成员增加或移除，群主变更，群公告变更），回调该事件。
        收到该事件后，企业需要再调用获取客户群详情接口，以获取最新的群详情。
        TODO
        :param chat_id:
        :return:
        """
        template = """<xml>
        <ToUserName><![CDATA[%(toUser)s]]></ToUserName>
        <FromUserName><![CDATA[sys]]></FromUserName>
        <CreateTime>%(CreateTime)s</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[change_external_chat]]></Event>
        <ChatId><![CDATA[%(ChatId)s]]></ChatId>
        <ChangeType><![CDATA[update]]></ChangeType>
        <UpdateDetail><![CDATA[add_member]]></UpdateDetail>
        <JoinScene>1</JoinScene>
        <QuitScene>0</QuitScene>
        <MemChangeCnt>10</MemChangeCnt>
        </xml>"""
        event_dict = {
            'toUser': self.corp_id,
            'CreateTime': self.createtime,
            'ChatId': chat_id
        }
        event_xml = template % event_dict
        return self.post_callback(self.url, event_xml, self.agent_id)

    # 客户群解散事件
    def dismiss_chat(self, chat_id):
        """
        客户群解散事件：当客户群被群主解散后，回调该事件。
        需注意的是，如果发生群信息变动，会立即收到此事件，但是部分信息是异步处理，
        可能需要等一段时间(例如2秒)调用获取客户群详情接口才能得到最新结果
        :param chat_id:
        :return:
        """
        template = """<xml>
        <ToUserName><![CDATA[%(toUser)s]]></ToUserName>
        <FromUserName><![CDATA[sys]]></FromUserName>
        <CreateTime>%(CreateTime)s</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[change_external_chat]]></Event>
        <ChatId><![CDATA[%(ChatId)s]]></ChatId>
        <ChangeType><![CDATA[dismiss]]></ChangeType>
        </xml>"""
        event_dict = {
            'toUser': self.corp_id,
            'CreateTime': self.createtime,
            'ChatId': chat_id
        }
        event_xml = template % event_dict
        return self.post_callback(self.url, event_xml, self.agent_id)

    # 企业客户标签创建事件
    def create_tag(self, tag_id):
        """
        企业客户标签创建事件：企业/管理员创建客户标签/标签组时，回调此事件。
        收到该事件后，企业需要调用获取企业标签库来获取标签/标签组的详细信息。
        :return:
        """
        template = """<xml>
        <ToUserName><![CDATA[%(toUser)s]]></ToUserName>
        <FromUserName><![CDATA[sys]]></FromUserName> 
        <CreateTime>%(CreateTime)s</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[change_external_tag]]></Event>
        <Id><![CDATA[%(TAG_ID)s]]></Id>
        <TagType><![CDATA[tag]]></TagType>
        <ChangeType><![CDATA[create]]></ChangeType>
        </xml>"""
        event_dict = {
            'toUser': self.corp_id,
            'CreateTime': self.createtime,
            'TAG_ID': tag_id,
        }
        event_xml = template % event_dict
        return self.post_callback(self.url, event_xml, self.agent_id)

    # 企业客户标签变更事件
    def update_tag(self, tag_id):
        """
        企业客户标签变更事件：当企业客户标签/标签组被修改时，回调此事件。
        收到该事件后，企业需要调用获取企业标签库来获取标签/标签组的详细信息。
        :return:
        """
        template = """<xml>
        <ToUserName><![CDATA[%(toUser)s]]></ToUserName>
        <FromUserName><![CDATA[sys]]></FromUserName> 
        <CreateTime>%(CreateTime)s</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[change_external_tag]]></Event>
        <Id><![CDATA[%(TAG_ID)s]]></Id>
        <TagType><![CDATA[tag]]></TagType>
        <ChangeType><![CDATA[update]]></ChangeType>
        </xml>"""
        event_dict = {
            'toUser': self.corp_id,
            'CreateTime': self.createtime,
            'TAG_ID': tag_id
        }
        event_xml = template % event_dict
        return self.post_callback(self.url, event_xml, self.agent_id)

    # 企业客户标签删除事件
    def delete_tag(self, tag_id):
        """
        企业客户标签删除事件：当企业客户标签/标签组被删除改时，回调此事件。
        删除标签组时，该标签组下的所有标签将被同时删除，但不会进行回调。
        :return:
        """
        template = """<xml>
        <ToUserName><![CDATA[%(toUser)s]]></ToUserName>
        <FromUserName><![CDATA[sys]]></FromUserName> 
        <CreateTime>%(CreateTime)s</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[change_external_tag]]></Event>
        <Id><![CDATA[%(TAG_ID)s]]></Id>
        <TagType><![CDATA[tag]]></TagType>
        <ChangeType><![CDATA[delete]]></ChangeType>
        </xml>
        """
        event_dict = {
            'toUser': self.corp_id,
            'CreateTime': self.createtime,
            'TAG_ID': tag_id
        }
        event_xml = template % event_dict
        return self.post_callback(self.url, event_xml, self.agent_id)


class ExternalContactTestCase(unittest.TestCase):

    def setUp(self):
        self.ec = CallBackExternalContact(1)
        self.ec.agent_id = "1000002"

    def atest_add_external_contact(self):
        logger.info("添加企业客户事件：")
        self.ec.add_external_contact("XuTao", "wm-6mmCAAAIwZUEGNnUi8227GpFApaaQ")

    def test_edit_external_contact(self):
        logger.info("编辑企业客户事件：")
        self.ec.edit_external_contact("XuTao", "wm-6mmCAAAIwZUEGNnUi8227GpFApaaQ")

    def test_delete_tag(self):
        logger.info("编辑企业客户事件：")
        self.ec.delete_tag("et-6mmCAAA5-98JHcLjG-Kdk-ndw3sPQ")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ExternalContactTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
