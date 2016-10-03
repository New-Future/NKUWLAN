#!/usr/bin/python
# encoding=utf-8
# coding:utf-8
import nkuwlan.gateway as gateway
import time
import socket

account = "网关账号[学号]"
password = "网关登录密码"
cir_time = 30  # 循环秒数
timeout = 30  # 连接超时

socket.setdefaulttimeout(cir_time)

while True:
    print time.ctime()
    result = gateway.query()
    if result == None or result['uid'] == None:
        print 'OFFline, try login: ', gateway.login(account, password)
    else:
        print 'ONline: ', result
    time.sleep(cir_time)  # 每隔cir_time秒执行一次
