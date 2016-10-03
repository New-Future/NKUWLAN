# encoding=utf-8
# coding:utf-8
'''
南开网关(NKU_WLAN)操作pyhton核心库，包括：登录，查询，注销
the lib for NKU Gateway,Contains Login，Query，and Logout
@version: 1.0.0
@author: New Future
'''
__version__ = '1.0.0'
__author__ = 'New Future'
__all__ = ["login", "logout", "query", "error"]

import urllib2
import urllib

# 网关 地址
host = ['http://202.113.18.110', 'http://202.113.18.210']
# url路径
query_path = '/'
login_path = ':801/eportal/?c=ACSetting&a=Login'
logout_path = ':801/eportal/?c=ACSetting&a=Logout'

NET_ERROR = None

# 注销


def logout():
    for h in host:
        request(h + logout_path)

# 查找


def find(content, start, endtag="'"):
    p = content.find(start)
    if p > 0:
        content = content[len(start) + p:]
        end = content.find(endtag)
        f = content[:end]
        return f.strip()

# 获取网页


def request(url, data=None):
    global NET_ERROR
    try:
        urllib2.getproxies = lambda: {}
        req = urllib2.urlopen(url, data)
        return req.read()
    except Exception as e:
        NET_ERROR = e
        return None

# 查询


def query(qhost=None):
    # 主机列表
    if qhost == None:
        hostList = host
    elif type(qhost) is str:
        hostList = [qhost]
    else:
        hostList = qhost
    # 逐个查询直到命中
    result = None
    for h in hostList:
        html = request(h)
        if html == None:  # 网关异常直接换其他网关
            continue
        else:
            uid = find(html, "uid='")
            flow = find(html, "flow='")
            flow = int(flow) if flow else 0
            fee = find(html, "fee='")
            fee = int(fee) if flow else 0
            ipv4 = find(html, "v4ip='")
            result = {'uid': uid, 'fee': fee,
                      'flow': flow / 1024, 'ipv4': ipv4}
            if uid != None:  # 查询到登录ID返回
                return result
            else:
                continue

    return result

# 登录


def login(user, pwd):
    data = {'DDDDD': user, 'upass': pwd}
    data = urllib.urlencode(data)
    for h in host:
        url = h + login_path
        request(url, data)
        result = query(h)
        if result != None and result['uid'] != None:
            return result
# 获取错误信息


def error():
    return NET_ERROR

if __name__ == '__main__':
    print(query(host))
