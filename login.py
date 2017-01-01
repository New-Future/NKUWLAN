#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from nkuwlan.config import save_conf, load_conf, delete_conf
from nkuwlan.gateway import login, logout, query, error
import sys
import time


# START_TAG #
from socket import setdefaulttimeout
try:
    input = raw_input
except NameError:
    pass

# 配置
account = None  # "网关账号[学号]"
password = None  # 网关登录密码
cir_time = 60  # 循环时间(s)
TIMEOUT = 10  # 连接超时时间(s)

setdefaulttimeout(TIMEOUT)


def getAccount(autoload=True, internal=1):  # 获取账号
    global account, password
    import getpass
    conf = autoload and load_conf()
    if conf:
        account = conf["username"]
        password = conf["password"]
    else:
        print (sys.argv[0], "-s to save")
        account = input("input username:")
        password = getpass.getpass("input password:")
    return login(account, password, internal)


def auto(internal=0):  # 自动登陆
    setdefaulttimeout(4)
    result = query()
    setdefaulttimeout(TIMEOUT)

    if result and result['uid']:
        print('ONLine: ', result)
        return True
    else:
        print('OFFLine, try login!')
        getAccount(internal=internal)
        result = login(account, password, internal)
        if result:
            print('Login SUCCESS:', result)
            return True
        else:
            return False


def loop():  # 循环登录
    global password
    if not load_conf():
        setdefaulttimeout(2)
        logout()

    setdefaulttimeout(3)
    while not getAccount():
        password = None
        print ("%s try login fialed!\n%s" % (account, error()))
    else:
        print ("Login SUCCESS!")

    setdefaulttimeout(TIMEOUT)
    while True:
        print (time.ctime())
        if auto():
            time.sleep(cir_time)  # 每隔cir_time秒执行一次
        else:
            time.sleep(cir_time / 5)  # 每隔cir_time秒执行一次


def save():  # 保存账号
    conf = {
        "username": account,
        "password": password,
    }
    result = save_conf(conf)
    if result:
        print("saved to", result)
        return True
    else:
        print ("save failed!")

if __name__ == '__main__':
    print("Login NKUWlan")
    if len(sys.argv) > 1:
        account = sys.argv[1]
    if len(sys.argv) > 2:
        password = sys.argv[2]
    print("waiting...")
    loop()
