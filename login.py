#!/usr/bin/python
# -*- coding: utf-8 -*-

from nkuwlan.gateway import *
from nkuwlan.config import *
#START_TAG
import sys
import socket

# 配置
account  = None #"网关账号[学号]"
password = None #网关登录密码
cir_time = 60   #循环时间(s)
TIMEOUT  = 10   #连接超时时间(s)

socket.setdefaulttimeout(TIMEOUT)


def getAccount(autoload=True): #获取账号
    import getpass
    global account,password
    conf = autoload and load_conf()
    if conf:
        account  = conf["username"]
        password = conf["password"]
    account = account or raw_input("input username [ 学号或账号 ]:")
    password = password or getpass.getpass("input password [ 校园网密码 ]:")
    return login(account,password)
        
def auto():  #自动登陆
    global account,password

    socket.setdefaulttimeout(4)
    result = query()
    socket.setdefaulttimeout(TIMEOUT)
    
    if result and result['uid']:
        print 'ONLine: ', result
        return True
    else:
        print 'OFFLine, try login!'
        getAccount()
        result = login(account, password)
        if result:
            print 'Login SUCCESS:', result
            return True
        else:
            return False

def loop(): #循环登录
    import time
    global cir_time,TIMEOUT,account,password
    if not load_conf():
        socket.setdefaulttimeout(2)
        logout()
    
    socket.setdefaulttimeout(3)
    while not getAccount():
        password=None
        print "%s try login fialed!"%account
        print error()
    else:
        print "Login SUCCESS! [ 登录成功! ]"
    
    socket.setdefaulttimeout(TIMEOUT)
    while True:
        print time.ctime()
        if auto():
            time.sleep(cir_time) #每隔cir_time秒执行一次
        else:
            time.sleep(cir_time/5) #每隔cir_time秒执行一次


def save():#保存账号
    conf={
        "version":__version__,
        "username":account,
        "password":password,
    }
    result = save_conf(conf)
    if result:
        print "saved to %s"%result
        return True
    else:
        print "save failed!"
        return False

if __name__ == '__main__':
    print "Login NKUWlan"
    if len(sys.argv) > 1 : account = sys.argv[1]
    if len(sys.argv) > 2 : password = sys.argv[2]
    print "waiting..."
    loop()
    