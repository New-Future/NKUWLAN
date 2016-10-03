#!/usr/bin/python
# encoding=utf-8
# coding:utf-8
from nkuwlan.gateway import logout

# START_TAG #


def logoutAccount():
    print "wait..."
    logout()
    print '\nlogout success!'


if __name__ == '__main__':
    logoutAccount()
