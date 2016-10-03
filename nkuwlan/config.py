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
__version__ = '1.0.0'
__author__ = 'New Future'
__all__ = ["get_conf_file", "load_conf", "save_conf", "delete_conf"]

import os
import json
import sys
import base64
from distutils.version import StrictVersion

pathlist = [
    os.path.expanduser('~') + '/.nkuwlan/conf.json',
    os.path.expanduser('~') + '/.nkuwlan.json',
    '/etc/nkuwlan/conf.json',
]

# 获取配置文件


def get_conf_file():
    for fname in pathlist:
        if os.path.isfile(fname):
            return fname

# 读取配置


def load_conf():
    fname = get_conf_file()
    if fname:
        try:
            with open(fname, 'r') as configure_file:
                conf = json.load(configure_file)
                conf["password"] = decode(conf['username'], conf[
                                          'password'], conf['version'])
                return conf
        except Exception as e:
            print('load config failed: %s' % e)
            return False

# 保存配置


def save_conf(conf):
    fname = get_conf_file() or pathlist[0]
    dir = os.path.dirname(fname)
    try:
        if not os.path.exists(dir):
            os.mkdir(dir, 0o700)
        with os.fdopen(os.open(fname, os.O_WRONLY | os.O_TRUNC | os.O_CREAT, 0o600), 'w') as handle:
            conf['version'] = __version__
            conf["password"] = encode(conf['username'], conf[
                                      'password'], conf['version'])
            handle.write(json.dumps(conf))
            return fname
    except Exception as e:
        print("save error: %s" % e)
        return False

# 删除配置文件


def delete_conf(conf):
    fname = get_conf_file()
    if fname:
        os.remove(fname)

# 加密


def encode(key, pwd, version=None):
    enc = []
    for i in range(len(pwd)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(pwd[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    enc = "".join(enc)
    if sys.version_info[0] == 3:
        enc = enc.encode()
    return base64.urlsafe_b64encode(enc).decode()

# 解密


def decode(key, enc, version=None):
    if StrictVersion(version) < StrictVersion('1.0.0'):
        return enc
    dec = []
    enc = base64.urlsafe_b64decode(enc.encode())
    if sys.version_info[0] == 3:
        enc = enc.decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)
