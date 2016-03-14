#!/usr/bin/python
# encoding=utf-8
# 南开网关自动登陆单文件版

# 下面是配置
account = None
password = None
cir_time = 30  # s 循环时间
TIMEOUT = 30  # s 链接超时时间
# 下面是正文不用管

import urllib2
import urllib
import sys
import time
import getpass

# 网关 地址
host = ['http://202.113.18.110', 'http://202.113.18.210']
# url路径
query_path, login_path, logout_path = '/', ':801/eportal/?c=ACSetting&a=Login', ':801/eportal/?c=ACSetting&a=Logout'


def logout():  # 注销
    for h in host:
        request(h + logout_path)


def find(content, start, endtag="'"):  # 查找
    p = content.find(start)
    if p > 0:
        content = content[len(start) + p:]
        end = content.find(endtag)
        return content[:end].strip()


def request(url, data=None, timeout=TIMEOUT):  # 获取网页
    try:
        return urllib2.urlopen(url, data, timeout=TIMEOUT).read()
    except Exception, e:
        return None


def query(qhost=None):  # 查询

    if qhost == None:
        hostList = host
    elif type(qhost) is str:
        hostList = [qhost]
    else:
        hostList = qhost
    result = None
    for h in hostList:    # 逐个查询直到命中
        html = request(h)
        if html == None:  # 网关异常直接换其他网关
            continue
        else:
            flow, uid, fee = find(html, "flow='"), find(html, "uid='"), find(html, "fee='")
            result = {'uid': uid, 'fee': fee, 'flow': flow}
            if uid != None:  # 查询到登录ID返回
                return result
    return result


def login(user, pwd):  # 登录
    data = {'DDDDD': user, 'upass': pwd}
    data = urllib.urlencode(data)
    for h in host:
        url = h + login_path
        request(url, data)
        result = query(h)
        if result != None and result['uid'] != None:
            return result


def auto(user, pwd):  # 自动登陆
    result = query()
    if result == None or result['uid'] == None:
        print 'OFFLine, try login!'
        result = login(account, password)
        if result:
            print 'Login SUCCESS:', result
            return True
    else:
        print 'ONLine: ', result

if __name__ == '__main__':
    cmd = len(sys.argv) > 1 and sys.argv[1]
    if cmd and cmd.lower() == "logout":  # 注销命令
        logout()
        print "Logout!"
    else:
        print "NKU GATEWAY auto login"
        account = account or raw_input("input username [student id]:")
        password = password or getpass.getpass("input password [no display]:")
        print 'start!\n\r'
        while cmd or not auto(account, password):
            print time.ctime()
            time.sleep(cir_time)  # 每隔cir_time秒循环一次
