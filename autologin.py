#!/usr/bin/python
#encoding=utf-8
#coding:utf-8
import gateway
import time

account='12344'
pwd='password'
cir_time=60 #循环秒数

while True:
	result=gateway.query()
	if result==None or result['uid']==None:
		print 'LOGIN:',gateway.login(account,pwd)
	else:
		print result
	print time.ctime()
	time.sleep(cir_time)#每隔1秒执行一次