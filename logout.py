#!/usr/bin/python
# encoding=utf-8
# coding:utf-8
from nkuwlan.gateway import logout

# START_TAG #


def logoutAccount():
    print "logout..."
    logout()
    print 'Done!'


if __name__ == '__main__':
    logoutAccount()
