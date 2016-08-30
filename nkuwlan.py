#!/usr/bin/python
# -*- coding: utf-8 -*-
# build at Tue Aug 30 04:12:16 2016
__version__ = '0.1.3'

#include form file [gateway.py] 
import urllib2
import urllib

#网关 地址
host = ['http://202.113.18.110','http://202.113.18.210']
#url路径
query_path='/'
login_path=':801/eportal/?c=ACSetting&a=Login'
logout_path=':801/eportal/?c=ACSetting&a=Logout'

NET_ERROR=None

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
	global NET_ERROR
	try:
		urllib2.getproxies = lambda: {}
		req=urllib2.urlopen(url,data)
		return req.read()
	except Exception, e:
		NET_ERROR = e
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
			uid  = find(html,"uid='")
			flow = find(html,"flow='")
			flow = int(flow) if flow else 0
			fee  = find(html,"fee='")
			fee  = int(fee) if flow else 0 
			ipv4 = find(html,"v4ip='")
			result={'uid':uid,'fee':fee,'flow':flow/1024,'ipv4':ipv4}
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


#include form file [config.py] 
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



#include form file [login.py] 
#START_TAG
import sys
import socket

# 配置
account  = None #"网关账号[学号]"
password = None #网关登录密码
cir_time = 60   #循环时间(s)
TIMEOUT  = 10   #连接超时时间(s)

socket.setdefaulttimeout(TIMEOUT)


def getAccount(autoload=True): #获取账号
    import getpass
    global account,password
    conf = autoload and load_conf()
    if conf:
        account  = conf["username"]
        password = conf["password"]
    account = account or raw_input("input username [ 学号或账号 ]:")
    password = password or getpass.getpass("input password [ 校园网密码 ]:")
    return login(account,password)
        
def auto():  #自动登陆
    global account,password

    socket.setdefaulttimeout(4)
    result = query()
    socket.setdefaulttimeout(TIMEOUT)
    
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

def loop(): #循环登录
    import time
    global cir_time,TIMEOUT,account,password
    if not load_conf():
        socket.setdefaulttimeout(2)
        logout()
    
    socket.setdefaulttimeout(3)
    while not getAccount():
        password=None
        print "%s try login fialed!"%account
        print NET_ERROR
    else:
        print "Login SUCCESS! [ 登录成功! ]"
    
    socket.setdefaulttimeout(TIMEOUT)
    while True:
        print time.ctime()
        if auto():
            time.sleep(cir_time) #每隔cir_time秒执行一次
        else:
            time.sleep(cir_time/5) #每隔cir_time秒执行一次


def save():#保存账号
    conf={
        "version":__version__,
        "username":account,
        "password":password,
    }
    result = save_conf(conf)
    if result:
        print "saved to %s"%result
        return True
    else:
        print "save failed!"
        return False


#include form file [logout.py] 
#START_TAG
def logoutAccount():
    print "waiting..."
    logout()
    print 'logout success![ 校园网已注销 ]'




if __name__ == "__main__":
    cmd = len(sys.argv) > 1 and sys.argv[1].lower()
    if not cmd:
        auto()
    elif cmd == "logout":
        logoutAccount()
    elif cmd == "-s":
        logoutAccount()
        if getAccount(False): save()
    elif cmd == "-v":
        print "NKUWLAN (python) verison :",__version__
    else :
        loop()
