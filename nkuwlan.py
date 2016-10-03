#!/usr/bin/env python
# -*- coding: utf-8 -*-
__version__ = '1.1.2'
__author__ = 'New Future'

# THIS FILE BUILD AT--- Mon Oct  3 13:55:18 2016

#include form file [nkuwlan/gateway.py] 
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
    if type(qhost) is str:  # 指定主机
        hostList = [qhost]
    elif qhost:  # 数组
        hostList = qhost
    else:  # 默认
        hostList = host
    # 逐个查询直到命中
    for h in hostList:
        html = request(h)
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
        if result and result['uid']:
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
        f = content[:content.find(endtag)]
        return f.strip()


def request(url, data=None):  # 获取网页
    try:
        urllib2.getproxies = lambda: {}
        return urllib2.urlopen(url, data).read()
    except Exception as e:
        NET_ERROR = e
        return None



#include form file [nkuwlan/config.py] 
import os
import json
import sys
import base64
import time
from hashlib import sha512
from uuid import getnode
from distutils.version import StrictVersion

_user_path = os.path.expanduser('~')
pathlist = [
    _user_path + '/.nkuwlan/conf.json',
    _user_path + '/.nkuwlan.json',
    '/etc/nkuwlan/conf.json',
]


def load_conf(fname=None):
    """load config form the config file.

     从文件(json格式)中读取配置,并根据版本对密码解密和校验
     如果文件中不包含版本信息不对密码解密

    Args:
        fname: 文件名(配置的json文件)，如果不指定会尝试系统默认的文件列表 pathlist

    Returns:
        包含配置信息的字典;
        如果配置不存在返回None;
        如果加载出错返回False;

    Raises:

    """
    fname = get_conf_file(fname)
    if fname:
        try:
            with open(fname, 'r') as configure_file:
                conf = json.load(configure_file)
                if "version" in conf:  # 包含version 解密
                    conf["password"] = decode(conf, fname)
                    if not conf["password"]:
                        return False
                return conf
        except Exception as e:
            print('load config failed: %s' % e)
            return False


def save_conf(conf, fname=None):  # 保存配置
    """save config to the config file.

     保存配置到文件，并对密码加密

    Args:
        conf：配置字典包括"username"和"password"
        fname: 保存的文件名绝对路径(json)，如果不指定会尝试系统默认的文件列表 pathlist

    Returns:
        fname: 保存成功返回文件名
        False： 保存出错

    Raises:

    """

    fname = get_conf_file(fname) or pathlist[0]
    dir = os.path.dirname(fname)
    try:
        if not os.path.exists(dir):
            os.mkdir(dir, 0o700)
        if not os.path.isfile(fname):
            if os.name == 'nt':  # windows
                open(fname, 'w').close()
            else:
                os.mknod(fname, 0o600)

        conf['version'] = __version__
        conf["password"], atime, mtime = encode(conf, fname)

        with open(fname, 'w') as f:
            f.write(json.dumps(conf))
        os.utime(fname, (atime, mtime))  # 跟新文件校验时间戳
        return fname

    except Exception as e:
        print("save error: %s" % e)
        return False


def delete_conf(fname=None):  # 删除配置文件
    """delete config file.

    删除配置文件

    Args:
        fname: 保存的文件名绝对路径(json)，如果不指定会尝试系统默认的文件列表 pathlist

    Returns:
        fname: 删除的文件名
        False： 无可删除配置文件

    Raises:
    """
    fname = get_conf_file(fname)
    if fname:
        os.remove(fname)
        return fname


def get_conf_file(fname=None):  # 获取配置文件
    if fname:
        return fname
    for fname in pathlist:
        if os.path.isfile(fname):
            return fname


def encode(conf, path):  # 加密
    h = key_info(path)
    atime, mtime = round(time.time()) + 10, round(h['CT'])  # 修改文件时间
    h['AT'], h['MT'] = float(atime), float(mtime)
    key, start, end = key_gen(h, conf['username'])

    pwd = start + conf['password'] + end
    enc = []
    for i in range(len(pwd)):
        enc_c = chr((ord(pwd[i]) + ord(key[i % len(key)])) % 256)
        enc.append(enc_c)
    enc = "".join(enc)
    if sys.version_info[0] == 3:  # for python 3
        enc = enc.encode()
    enc = base64. urlsafe_b64encode(enc).decode()

    return [enc, atime, mtime]


def decode(conf, path):  # 解密
    if StrictVersion(conf['version']) < StrictVersion('1.0.0'):
        return conf['password']
    # 计算唯一加密密钥
    h = key_info(path)
    key, start, end = key_gen(h, conf['username'])

    # 加密后密码
    enc = conf['password'].encode()
    enc = base64.urlsafe_b64decode(enc)
    if sys.version_info[0] == 3:
        enc = enc.decode()

    dec = []
    for i in range(len(enc)):
        dec_c = chr((ord(enc[i]) - ord(key[i % len(key)])) % 256)
        dec.append(dec_c)
    dec = "".join(dec)  # 解密后的密码

    # print (dec)
    # 校验
    if dec.startswith(start) and dec.endswith(end):
        return dec[len(start):-len(end)]
    else:  # 校验失败
        print("\nconfig file verification failed!")
        return False


def key_info(fname):  # 获取每台机器唯一的加密密钥和验证key
    stats = os.stat(fname)  # 文件属性
    return {
        'P': fname,  # 文件路径hash
        'mac': getnode(),  # MAC地址
        'M': stats.st_mode,
        'N': stats.st_ino,
        'D': stats.st_dev,
        'L': stats.st_nlink,
        'U': stats.st_uid,
        'G': stats.st_gid,
        'CT': stats.st_ctime,
        'AT': stats.st_atime,
        'MT': stats.st_mtime,
    }


def key_gen(h, username):  # 生密钥和首尾校验码
    h['CT'] = 0  # ctime always change
    # print (repr(sorted(h.items())))
    h = sha512(repr(sorted(h.items())).encode('utf-8')).hexdigest()
    key = sha512((username + h).encode('utf-8')).hexdigest()
    hi = str(int(h, 16))
    start, end = h[:int(hi[3])], h[-int(hi[-1]):]
    return [key, start, end]

#include form file [login.py] 
# START_TAG #
from socket import setdefaulttimeout

# 配置
account = None  # "网关账号[学号]"
password = None  # 网关登录密码
cir_time = 60  # 循环时间(s)
TIMEOUT = 10  # 连接超时时间(s)

setdefaulttimeout(TIMEOUT)


def getAccount(autoload=True):  # 获取账号
    global account, password
    import getpass
    conf = autoload and load_conf()
    if conf:
        account = conf["username"]
        password = conf["password"]
    else:
        account = raw_input("input username:")
        password = getpass.getpass("input password:")
    return login(account, password)


def auto():  # 自动登陆
    setdefaulttimeout(4)
    result = query()
    setdefaulttimeout(TIMEOUT)

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


def loop():  # 循环登录
    global password
    if not load_conf():
        setdefaulttimeout(2)
        logout()

    setdefaulttimeout(3)
    while not getAccount():
        password = None
        print "%s try login fialed!\n%s" % (account, error())
    else:
        print "Login SUCCESS!"

    setdefaulttimeout(TIMEOUT)
    while True:
        print time.ctime()
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
        print "saved to " + result
        return True
    else:
        print "save failed!"


#include form file [logout.py] 
# START_TAG #


def logoutAccount():
    print "wait..."
    logout()
    print '\nlogout success!'



if __name__ == "__main__":
    cmd = sys.argv[1:] and sys.argv[1].lower()
    
    if cmd == "logout":
        logoutAccount()
    elif cmd == "-s":
        logoutAccount()
        if getAccount(False): save()
    elif cmd == "-v":
        print "NKUWLAN verison :",__version__
    elif cmd:
        loop()
    else:
        auto()
