#!/usr/bin/env python
# encoding=utf-8
# coding:utf-8
from __future__ import print_function
from nkuwlan.gateway import logout

# START_TAG #


def logout_account():  # 注销
    '''
    注销登录
    '''
    print("logout...")
    logout()
    print('Done!')


if __name__ == '__main__':
    logout_account()
