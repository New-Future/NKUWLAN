#!/usr/bin/env python
from __future__ import print_function;__version__='2.2.0';__author__='New Future'
try:import urllib2 as E;from urllib import urlencode as ay
except ImportError:import urllib.request as E;from urllib.parse import urlencode as ay
F='http://202.113.18.106',;ax='/';ac=':801/eportal/?c=ACSetting&a=Login';ad=':801/eportal/?c=ACSetting&a=Logout';O=None
def P(*G):
	if len(G)<=0:G=F
	for q in G:
		u=H(q)
		if u:
			Q=find(u,"flow='");R=find(u,"fee='");d={'fee':R and int(R),'flow':Q and int(Q)/1024,'uid':find(u,"uid='"),'ipv4':find(u,"v4ip='")}
			if d['uid']:return d
def S(T,y,internal=0):
	k={'upass':y}
	if internal:k.update(DDDDD='_'+T,login_nei=1)
	else:k['DDDDD']=T
	for q in F:
		I=q+ac;H(I,k);d=P(q)
		if d and d['uid']:return d
def U():
	for q in F:H(q+ad)
def error():return O
def find(v,h,ae="'"):
	V=v.find(h)
	if V>0:v=v[len(h)+V:];return v[:v.find(ae)].strip()
def H(I,k=None,af='gb2312'):
	try:k=k and ay(k).encode();E.getproxies=lambda:{};return E.urlopen(I,k).read().decode(af)
	except Exception,ag:O=ag;return None
import base64 as ao;import json as ai;import os as g;import sys as B;import time as L;from distutils.version import StrictVersion as ap;from hashlib import sha512 as at;from uuid import getnode as aA;_a=g.path.expanduser('~');W=[_a+'/.nkuwlan/conf.json',_a+'/.nkuwlan.json','/etc/nkuwlan/conf.json']
def X(a=None):
	a=J(a)
	if a:
		try:
			w=Y(a)
			with open(a,'r')as ah:
				b=ai.load(ah);b['password']=aj(b,w)
				if not b['password']:return False
			g.utime(a,(w['AT'],w['MT']));return b
		except Exception,K:print('load config failed: %s'%K);return False
def ak(b,a=None):
	a=J(a)or W[0];dirname=g.path.dirname(a)
	try:
		if not g.path.exists(dirname):g.mkdir(dirname,448)
		if not g.path.isfile(a):
			if g.name=='nt':open(a,'w').close()
			else:g.mknod(a,384)
		b['version']=__version__;b['password'],z,A=al(b,a)
		with open(a,'w')as am:am.write(ai.dumps(b))
		g.utime(a,(z,A));return a
	except Exception,K:print('save error: %s'%K);return False
def az(a=None):
	a=J(a)
	if a:g.remove(a);return a
def J(a=None):
	if a:return a
	for a in W:
		if g.path.isfile(a):return a
def al(b,path):
	f=Y(path);z,A=round(L.time())+10,round(f['CT']);f['AT'],f['MT']=float(z),float(A);n,h,r=Z(f,b['username']);y=h+b['password']+r;e=[]
	for i in range(len(y)):an=chr((ord(y[i])+ord(n[i%len(n)]))%256);e.append(an)
	e=''.join(e)
	if B.version_info[0]==3:e=e.encode()
	e=ao.urlsafe_b64encode(e).decode();return[e,z,A]
def aj(b,w):
	if not'version'in b or ap(b['version'])<ap('1.0.0'):return b['password']
	n,h,r=Z(w,b['username']);e=b['password'].encode();e=ao.urlsafe_b64decode(e)
	if B.version_info[0]==3:e=e.decode()
	s=[]
	for i in range(len(e)):aq=chr((ord(e[i])-ord(n[i%len(n)]))%256);s.append(aq)
	s=''.join(s)
	if s.startswith(h)and s.endswith(r):return s[len(h):-len(r)]
	else:print('\nconfig file verification failed!');return False
def Y(a):j=g.stat(a);return{'P':a,'mac':aA(),'M':j.st_mode,'N':j.st_ino,'D':j.st_dev,'L':j.st_nlink,'U':j.st_uid,'G':j.st_gid,'CT':j.st_ctime,'AT':j.st_atime,'MT':j.st_mtime}
def Z(f,ar):f['CT']=0;f=at(repr(sorted(f.items())).encode('utf-8')).hexdigest();n=at((ar+f).encode('utf-8')).hexdigest();aa=str(int(f,16));h,r=f[:int(aa[3])],f[-int(aa[-1]):];return[n,h,r]
from socket import setdefaulttimeout as x
try:input=raw_input
except NameError:0
o=None;l=None;ab=60;M=10;x(M)
def N(au=True,internal=1):
	global o,l;import getpass as aB;b=au and X()
	if b:o=b['username'];l=b['password']
	else:print(B.argv[0],'-s to save');o=input('input username:');l=aB.getpass('input password:')
	return S(o,l,internal)
def C(internal=0):
	x(4);d=P();x(M)
	if d and d['uid']:print('ONLine: ',d);return True
	else:
		print('OFFLine, try login!');N(internal=internal);d=S(o,l,internal)
		if d:print('Login SUCCESS:',d);return True
		else:return False
def av():
	global l
	if not X():x(2);U()
	x(3)
	while not N():l=None;print('%s try login fialed!\n%s'%(o,error()))
	else:print('Login SUCCESS!')
	x(M)
	while True:
		print(L.ctime())
		if C():L.sleep(ab)
		else:L.sleep(ab/5)
def aw():
	b={'username':o,'password':l};d=ak(b)
	if d:print('saved to',d);return True
	else:print('save failed!')
def D():print('logout...');U();print('Done!')
if __name__=='__main__':
	t=B.argv[1:]and B.argv[1].lower()
	if t=='logout':D()
	elif t=='loop':av()
	elif t=='-s':
		D()
		if N(False):aw()
	elif t=='nei':D();C(1)
	elif t=='wai':D();C()
	elif t=='-v':print(__version__)
	else:C()
