#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:address_book.py
@time:2021/08/13
@email:tao.xu2008@outlook.com
@description:
"""
import time
from config import cf, get_global_value
from custom_method.callback.base import CallBackRequest


class CallBackAddressBook(CallBackRequest):
    """通讯录回调"""

    def __init__(self, corp_id=None, token=None, aes_key=None, timestamp=None, nonce=None):
        test_env = get_global_value("test_env")
        self.corp_id = corp_id or cf.get_str(test_env, 'corp_id')
        self.token = token or cf.get_str(test_env, 'token')
        self.aes_key = aes_key or cf.get_str(test_env, 'aes_key')
        self.session_id = get_global_value("session_id")
        self.agent_id = get_global_value("login_agent_id")
        super(CallBackAddressBook, self).__init__(self.corp_id, self.token, self.aes_key, timestamp, nonce, self.session_id)
        self.createtime = str(int(time.time()))
        host = cf.get_str(test_env, 'host_mk')
        external_contact_path = "/wxwork/v1/callback/address_book"
        self.url = "{}{}/{}".format(host, external_contact_path, self.corp_id)

    # 成员变更通知 - 新增成员事件
    def create_user(self, user_id, name, department, mobile, email, avatar, telephone, address):
        """
        成员变更通知 - 新增成员事件
        :return:
        """
        template = """<xml>
        <ToUserName><![CDATA[%(toUser)s]]></ToUserName>
        <FromUserName><![CDATA[sys]]></FromUserName> 
        <CreateTime>%(CreateTime)s</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[change_contact]]></Event>
        <ChangeType>create_user</ChangeType>
        <UserID><![CDATA[%(UserID)s]]></UserID>
        <Name><![CDATA[%(Name)s]]></Name>
        <Department><![CDATA[%(Department)s]]></Department>
        <MainDepartment>1</MainDepartment>
        <IsLeaderInDept><![CDATA[1,0,0]]></IsLeaderInDept>
        <Position><![CDATA[产品经理]]></Position>
        <Mobile>%(Mobile)s</Mobile>
        <Gender>1</Gender>
        <Email><![CDATA[%(Email)s]]></Email>
        <Status>1</Status>
        <Avatar><![CDATA[%(Avatar)s]]></Avatar>
        <Alias><![CDATA[%(Alias)s]]></Alias>
        <Telephone><![CDATA[%(Telephone)s]]></Telephone>
        <Address><![CDATA[%(Address)s]]></Address>
        <ExtAttr>
            <Item>
            <Name><![CDATA[爱好]]></Name>
            <Type>0</Type>
            <Text>
                <Value><![CDATA[旅游]]></Value>
            </Text>
            </Item>
        </ExtAttr>
        </xml>"""
        event_dict = {
            'toUser': self.corp_id,
            'CreateTime': self.createtime,
            'UserID': user_id,
            'Name': name,
            'Department': department,
            'Mobile': mobile,
            'Email': email,
            'Avatar': avatar,
            'Telephone': telephone,
            'Address': address,
        }
        event_xml = template % event_dict
        return self.post_callback(self.url, event_xml, self.agent_id)


if __name__ == '__main__':
    pass
