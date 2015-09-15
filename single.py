#!/usr/bin/python
#encoding=utf-8
#coding:utf-8
'''
南开网关自动登陆单文件版
'''
##下面是配置
account  = None
password = None
cir_time = 30 #s
TIMEOUT  = 30 #s
#下面是正文不用管

import urllib2
import urllib
import time

#网关 地址
host = ['http://202.113.18.110','http://202.113.18.210']
#url路径
query_path='/'
login_path=':801/eportal/?c=ACSetting&a=Login'
logout_path=':801/eportal/?c=ACSetting&a=Logout'


#注销
def logout():
	for h in host:
		request(h+logout_path)

#查找
def find(content,start,endtag="'"):
	p=content.find(start)
	if p>0:
		content=content[len(start)+p:]
		end=content.find(endtag)
		f=content[:end];
		return f.strip()

#获取网页
def request(url,data=None,timeout=TIMEOUT):
	try:
		req=urllib2.urlopen(url,data,timeout=TIMEOUT)
		return req.read()
	except Exception, e:
		return None

#查询
def query(qhost=None):
	#主机列表
	if qhost==None:
		hostList=host
	elif type(qhost) is str:
		hostList=[qhost]
	else:
		hostList=qhost
	#逐个查询直到命中
	result=None
	for h in hostList:
		html=request(h)
		if html==None:#网关异常直接换其他网关
			continue
		else:
			flow=find(html,"flow='")
			uid=find(html,"uid='")
			fee=find(html,"fee='")
			result={'uid':uid,'fee':fee,'flow':flow}
			if uid!=None:#查询到登录ID返回
				return result
			else:
				continue
	return result

#登录
def login(user,pwd):
	data={'DDDDD':user,'upass':pwd}
	data=urllib.urlencode(data)
	for h in host:
		url=h+login_path
		request(url,data)
		result=query(h)
		if result!=None and result['uid']!=None:
			return result

#自动登陆
def auto(user,pwd):
	result=query()
	if result==None or result['uid']==None:
		print 'OFFline, try login: ',login(account,password)
	else:
		print 'ONline: ',result

print "NKU GATEWAY auto login"
if account==None:
	account = raw_input("input your account:")
else:
	print 'use account :',account
if password==None:
	password = raw_input("input your password:")

print 'start!\n\r\n\r'

while True:
	print time.ctime()
	auto(account,password)
	time.sleep(cir_time)#每隔cir_time秒执行一次