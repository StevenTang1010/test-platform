#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:base.py
@time:2021/08/12
@email:tao.xu2008@outlook.com
@description: 回调基础方法，如：数据加密
"""
import time
import unittest
import json
from loguru import logger
from runner.common.spiders.auth import Auth
from runner.pkgs.weworkapi_callback.WXBizMsgCrypt import WXBizMsgCrypt, XMLParse


class CallBackRequest(Auth, WXBizMsgCrypt):
    """回调请求处理：加密、请求"""
    def __init__(self, env_id, corp_id=None, token=None, aes_key=None, timestamp=None, nonce=None):
        Auth.__init__(self, env_id)
        self.corp_id = corp_id or self.env.config.get("corp_id").get("value")
        self.token = token or self.env.qw_external_contact_config.get("external_contact_token").get("value")
        self.aes_key = aes_key or self.env.qw_external_contact_config.get("external_contact_aes_key").get("value")
        WXBizMsgCrypt.__init__(self, self.token, self.aes_key, self.corp_id)

        self.timestamp = timestamp or str(int(time.time()))
        self.nonce = nonce or "1627750302"

    def test(self):
        """
        测试加密->解密
        :return:
        """
        msg = "哈哈哈哈"
        print("加密前：", msg)
        # 加密
        _, signature, encrypt = self.encrypt_msg(msg, self.nonce, self.timestamp)
        s_xml_encrypt_msg = self.encrypt_response_xml(encrypt, signature, self.timestamp, self.nonce)
        print("加密后：", encrypt)
        print("安全签名：", signature)
        # 解密
        _, s_msg = self.decrypt_msg(s_xml_encrypt_msg, signature, self.timestamp, self.nonce)
        print("解密后：", s_msg.decode('utf8'))

    def encrypt_text(self, text):
        """
        加密文本，用于Http Get请求验证URL有效性
        :param text:
        :return:
        """
        # 加密
        _, signature, encrypt = self.encrypt_msg(text, self.nonce, self.timestamp)
        logger.debug("加密后：{}".format(encrypt))
        logger.debug("安全签名：{}".format(signature))
        return signature, self.timestamp, self.nonce, encrypt

    def encrypt_receive_xml(self, data, to_user, to_agent_id):
        """
        加密被动响应包的数据，用于Http Post请求接收业务数据
        :param data: 事件消息体-xml
        :param to_user: 企业微信的CorpID，当为第三方应用回调事件时，CorpID的内容为suiteid
        :param to_agent_id: 接收的应用id，可在应用的设置页面获取。仅应用相关的回调会带该字段。
        :return:
        """
        _, signature, encrypt = self.encrypt_msg(json.dumps(data), self.nonce, self.timestamp)
        logger.debug("加密后：{}".format(encrypt))
        logger.debug("安全签名：{}".format(signature))
        encrypt_xml_msg = XMLParse().generate_receive_xml(to_user, to_agent_id, encrypt)
        return signature, encrypt_xml_msg

    def post_callback(self, url, event_xml, agent_id):
        """
        假设企业的接收消息的URL设置为 http://api.3dept.com。
        当用户触发回调行为时，企业微信会发送回调消息到填写的URL，请求内容如下：
        请求方式：POST
        请求地址 ：http://api.3dept.com/?msg_signature=ASDFQWEXZCVAQFASDFASDFSS&timestamp=13500001234&nonce=123412323
        接收数据格式 ：
        <xml>
           <ToUserName><![CDATA[toUser]]></ToUserName>
           <AgentID><![CDATA[toAgentID]]></AgentID>
           <Encrypt><![CDATA[msg_encrypt]]></Encrypt>
        </xml>
        :param url:
        :param event_xml:
        :param agent_id:
        :return:
        """
        logger.debug(event_xml)
        msg_signature, encpt_msg = self.encrypt_receive_xml(event_xml, self.corp_id, agent_id)
        logger.debug("{},{},{},{}".format(msg_signature, self.timestamp, self.nonce, encpt_msg))

        params = {
            "msg_signature": msg_signature,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
        }
        response = self.request("POST", url, params=params, data=encpt_msg)
        return response


class CallBackTestCase(unittest.TestCase):

    def setUp(self):
        self.corp_id = "ww0f7acb797142e8d3"
        self.agent_id = "1000002"
        token = "VgiYWMmCdYjTUAtuAxmk"
        aes_key = "srsbLGrXezOqRaHAmpCfBenBSVjeDMNZiuzrcOIGSFU"
        self.cbr = CallBackRequest(1, self.corp_id, token, aes_key)

    def test_1(self):
        print("测试加密解密：")
        self.cbr.test()

    def test_2(self):
        print("加密text:")
        text = '{"name":"C端用户", "id":"dasdahdhadak12313g8ad"}'
        print("加密前：{}".format(text))
        self.cbr.encrypt_text(text)

    def test_3(self):
        print("加密xml:")
        xml_str = """<xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[sys]]></FromUserName> 
            <CreateTime>1403610513</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[change_external_contact]]></Event>
            <ChangeType><![CDATA[add_external_contact]]></ChangeType>
            <UserID><![CDATA[zhangsan]]></UserID>
            <ExternalUserID><![CDATA[woAJ2GCAAAXtWyujaWJHDDGi0mAAAA]]></ExternalUserID>
            <State><![CDATA[teststate]]></State>
            <WelcomeCode><![CDATA[WELCOMECODE]]></WelcomeCode>
        </xml>"""
        print("加密前：{}".format(xml_str))
        self.cbr.encrypt_receive_xml(xml_str, self.corp_id, self.agent_id)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(CallBackTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
