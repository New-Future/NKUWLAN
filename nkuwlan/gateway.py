# encoding=utf-8
# coding:utf-8

'''
南开网关(NKU_WLAN)操作pyhton核心库，包括：登录，查询，注销
the lib for NKU Gateway,Contains Login，Query，and Logout
@version: 1.2.0
@author: New Future
@todo: 多线程或者异步请求
'''

__author__ = 'New Future'
__all__ = ["login", "logout", "query", "error"]

try:
    # python 2
    import urllib2 as req
    from urllib import urlencode
except ImportError:
    # python 3
    import urllib.request as req
    from urllib.parse import urlencode

# 网关 地址
HOST = ('http://202.113.18.106',)
# url路径
QUERY_PATH = '/'
LOGIN_PATH = ':801/eportal/?c=ACSetting&a=Login'
LOGOUT_PATH = ':801/eportal/?c=ACSetting&a=Logout'
# 错误信息
NET_ERROR = None


def query(*qhost):  # 查询
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
    if len(qhost) <= 0:
        # 指定主机使用默认
        qhost = HOST
    # 逐个查询直到命中
    for host in qhost:
        html = request(host)
        if html:  # 网关异常直接换其他网关
            flow = find(html, "flow='")
            fee = find(html, "fee='")
            result = {
                'fee': fee and int(fee),
                'flow': flow and int(flow) / 1024,
                'uid': find(html, "uid='"),
                'ipv4': find(html, "v4ip='")
            }
            if result['uid']:  # 查询到登录ID返回
                return result


def login(user, pwd, internal=0):  # 登录
    """login NKU_WLAN.

    登录网关

    Args:
        user: 登录账号 login account .
        pwd: 登录密码 password.
        internal: 是否只登录内网

    Returns:
        登录成功返回字典，显示账号当前信息；
        登录失败None

    Raises:

    """
    data = {'upass': pwd}
    if internal:
        data.update(DDDDD='_' + user, login_nei=1)
    else:
        data['DDDDD'] = user
    for host in HOST:
        url = host + LOGIN_PATH
        request(url, data)
        result = query(host)
        if result and result['uid']:
            return result


def logout():  # 注销
    """logout NKU_WLAN.

    注销网关尝试host列表的所有网关记录，一一注销
    """
    for host in HOST:
        request(host + LOGOUT_PATH)


def error():  # 获取错误信息
    """get last error info.

    获取上次出错信息

    Returns:
        Exception NET_ERROR
        未发生错误返回 None
    """
    return NET_ERROR


def find(content, start, endtag="'"):  # 查找
    """find string in html
        查找文档中start 和 end 之间的的内容
    Returns:
       string
    """
    pos = content.find(start)
    if pos > 0:
        content = content[len(start) + pos:]
        return content[:content.find(endtag)].strip()


def request(url, data=None, code='gb2312'):  # 获取网页
    """ resquet a url
        发送请求
    """
    try:
        data = data and urlencode(data).encode()
        req.getproxies = lambda: {}
        return req.urlopen(url, data).read().decode(code)
    except Exception as err:
        NET_ERROR = err
        return None


if __name__ == '__main__':
    print(query())
