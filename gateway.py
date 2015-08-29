#!/usr/bin/python
#encoding=utf-8
#coding:utf-8
'''
南开网关操作pyhton库，包括：登录，查询，注销
the lib for NKU Gateway,Contains Login，Query，and Logout
@version:0.1.0
@author:NewFuture
'''
__version__ = '0.1.0'
__author__='NewFuture'

import urllib2
import urllib

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
def request(url,data=None):
	try:
		req=urllib2.urlopen(url,data)
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

if __name__ == '__main__':
	result= query(host)
	print result