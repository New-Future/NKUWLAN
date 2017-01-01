# -*- coding: utf-8 -*-
# encoding=utf-8

'''
配置文件读写
配置文件优先级
'~/.nkuwlan/conf.json',#当前用户有效
'~/.nkuwlan.json',#当前用户有效
'/etc/nkuwlan/conf.json'#系统全局有效
文件权限0600
'''
# TODO 自动更新配置

from __future__ import print_function
from . import __version__

__author__ = 'New Future'
__all__ = ["load_conf", "save_conf", "delete_conf"]

# START_TAG #
import base64
import json
import os
import sys
import time
from distutils.version import StrictVersion
from hashlib import sha512
from uuid import getnode


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
            info = key_info(fname)
            with open(fname, 'r') as configure_file:
                conf = json.load(configure_file)
                conf["password"] = decode_password(conf, info)
                if not conf["password"]:
                    return False
            os.utime(fname, (info['AT'], info['MT']))  # 跟新文件校验时间戳
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
    dirname = os.path.dirname(fname)
    try:
        if not os.path.exists(dirname):
            os.mkdir(dirname, 0o700)
        if not os.path.isfile(fname):
            if os.name == 'nt':  # windows
                open(fname, 'w').close()
            else:
                os.mknod(fname, 0o600)

        conf['version'] = __version__
        conf["password"], atime, mtime = encode_password(conf, fname)

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


def encode_password(conf, path):  # 加密
    h = key_info(path)
    atime, mtime = round(time.time()) + 10, round(h['CT'])  # 修改文件时间
    h['AT'], h['MT'] = float(atime), float(mtime)
    key, start, end = key_gen(h, conf['username'])

    pwd = start + conf['password'] + end
    enc = []
    for i in range(len(pwd)):#range compatible for Python 3
        enc_c = chr((ord(pwd[i]) + ord(key[i % len(key)])) % 256)
        enc.append(enc_c)
    enc = "".join(enc)
    if sys.version_info[0] == 3:  # for python 3
        enc = enc.encode()
    enc = base64. urlsafe_b64encode(enc).decode()

    return [enc, atime, mtime]


def decode_password(conf, info):  # 解密

    if not 'version' in conf or StrictVersion(conf['version']) < StrictVersion('1.0.0'):
        return conf['password']
    # 计算唯一加密密钥
    key, start, end = key_gen(info, conf['username'])

    # 加密后密码
    enc = conf['password'].encode()
    enc = base64.urlsafe_b64decode(enc)
    if sys.version_info[0] == 3:
        enc = enc.decode()

    dec = []
    for i in range(len(enc)):#range compatible for Python 3
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
