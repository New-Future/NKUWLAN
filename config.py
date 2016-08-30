#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8

import os
import json

pathlist = [
    os.path.expanduser('~')+'/.nkuwlan/conf.json',
    os.path.expanduser('~')+'/.nkuwlan.json',
    '/etc/nkuwlan/conf.json',
]

def get_conf_file():
    for fname in pathlist:
        if os.path.isfile(fname):
            return fname

def load_conf():
    fname=get_conf_file()
    if fname:
        try:
            with open(fname,'r') as configure_file:
                return json.load(configure_file)
        except Exception,e:
            print e
            return False


def save_conf(conf):
    fname = get_conf_file() or pathlist[0]
    dir = os.path.dirname(fname)
    try:
        if not os.path.exists(dir):
            os.mkdir(dir,0700)
        with os.fdopen(os.open(fname, os.O_WRONLY | os.O_CREAT, 0600), 'w') as handle:
            handle.write(json.dumps(conf))
            return fname
    except Exception,e:
        print "save error",e
        return False



def delete_conf(conf):
    fname = get_conf_file()
    if fname:
        os.remove(fname)


