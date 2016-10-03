# encoding=utf-8
# coding:utf-8

'''
南开网关(NKU_WLAN)操作pyhton核心库，包括：登录，查询，注销
the lib for NKU Gateway,Contains Login，Query，and Logout
@version: 1.0.0
@author: New Future
'''

# TODO Python3 兼容.
# TODO 多线程或者异步请求

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
# 错误信息
NET_ERROR = None


def query(qhost=None):  # 查询
    """query info from NKU_WLAN.

    查询账号信息和登录状态

    Args:
        qhost: 查询主机，如果没有指定，会尝试主机列表所有主机 .

    Returns:
        查询成功返回字典，显示账号当前信息；
        查询失败None

    Raises:

    """
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
            result = {
                'uid': uid,
                'fee': fee,
                'flow': flow / 1024,
                'ipv4': ipv4
            }
            if uid != None:  # 查询到登录ID返回
                return result
            else:
                continue

    return result


def login(user, pwd):  # 登录
    """login NKU_WLAN.

    登录网关

    Args:
        user: 登录账号 login account .
        pwd:登录密码 password.

    Returns:
        登录成功返回字典，显示账号当前信息；
        登录失败None

    Raises:

    """
    data = {'DDDDD': user, 'upass': pwd}
    data = urllib.urlencode(data)
    for h in host:
        url = h + login_path
        request(url, data)
        result = query(h)
        if result != None and result['uid'] != None:
            return result


def logout():  # 注销
    """logout NKU_WLAN.

    注销网关尝试host列表的所有网关记录，一一注销
    """
    for h in host:
        request(h + logout_path)


def error():  # 获取错误信息
    """get last error info.

    获取上次出错信息

    Returns:
        Exception NET_ERROR
        未发生错误返回 None

    """
    return NET_ERROR


def find(content, start, endtag="'"):  # 查找
    p = content.find(start)
    if p > 0:
        content = content[len(start) + p:]
        end = content.find(endtag)
        f = content[:end]
        return f.strip()


def request(url, data=None):  # 获取网页
    global NET_ERROR
    try:
        urllib2.getproxies = lambda: {}
        req = urllib2.urlopen(url, data)
        return req.read()
    except Exception as e:
        NET_ERROR = e
        return None


if __name__ == '__main__':
    print(query(host))
