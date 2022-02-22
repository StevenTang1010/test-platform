#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:console_output.py
@time:2021/12/08
@email:tao.xu2008@outlook.com
@description:控制台输出 - 实时
"""

from django.shortcuts import render
from django.http import HttpResponse
from dwebsocket.decorators import accept_websocket


@accept_websocket
def output(request):
    if request.is_websocket():
        print(1)
        request.websocket.send('下载完成'.encode('utf-8'))
    if not request.is_websocket():
        # 判断是不是websocket连接
        try:
            message = request.GET['message']
            # 如果是普通的http方法
            return HttpResponse(message)
        except:
            return render(request, 'index.html')
    else:
        for message in request.websocket:
            message = message.decode('utf-8')
            # 接收前端发来的数据
            print(message)
            if message == 'connect_websocket':
                with open('./a.log') as f:
                    # 读取日志
                    f.seek(0, 2)
                    while True:
                        line = f.readline().strip()
                        if line:
                            print(line)
                            request.websocket.send(line.encode('utf-8'))
                            # 发送消息到客户端
            else:
                request.websocket.send('sorry!'.encode('utf-8'))


if __name__ == '__main__':
    pass
