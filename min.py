#!/usr/bin/env python
__version__='2.1.0';__author__='New Future'
try:import urllib2 as C;from urllib import urlencode as az
except ImportError:import urllib.request as C;from urllib.parse import urlencode as az
D='http://202.113.18.106',;ay='/';ac=':801/eportal/?c=ACSetting&a=Login';ad=':801/eportal/?c=ACSetting&a=Logout';M=None
def N(*E):
	if len(E)<=0:E=D
	for q in E:
		t=F(q)
		if t:
			O=find(t,"flow='");P=find(t,"fee='");d={'fee':P and int(P),'flow':O and int(O)/1024,'uid':find(t,"uid='"),'ipv4':find(t,"v4ip='")}
			if d['uid']:return d
def Q(R,x,ae=0):
	k={'upass':x}
	if ae:k.update(DDDDD='_'+R,login_nei=1)
	else:k['DDDDD']=R
	for q in D:
		G=q+ac;F(G,k);d=N(q)
		if d and d['uid']:return d
def S():
	for q in D:F(q+ad)
def error():return M
def find(u,h,af="'"):
	T=u.find(h)
	if T>0:u=u[len(h)+T:];return u[:u.find(af)].strip()
def F(G,k=None,ag='gb2312'):
	try:k=k and az(k).encode();C.getproxies=lambda:{};return C.urlopen(G,k).read().decode(ag)
	except Exception,ah:M=ah;return None
import base64 as ap;import json as aj;import os as g;import sys as A;import time as J;from distutils.version import StrictVersion as aq;from hashlib import sha512 as au;from uuid import getnode as aB;_a=g.path.expanduser('~');U=[_a+'/.nkuwlan/conf.json',_a+'/.nkuwlan.json','/etc/nkuwlan/conf.json']
def V(a=None):
	a=H(a)
	if a:
		try:
			v=W(a)
			with open(a,'r')as ai:
				b=aj.load(ai);b['password']=ak(b,v)
				if not b['password']:return False
			g.utime(a,(v['AT'],v['MT']));return b
		except Exception,I:print'load config failed: %s'%I;return False
def al(b,a=None):
	a=H(a)or U[0];dir=g.path.dirname(a)
	try:
		if not g.path.exists(dir):g.mkdir(dir,448)
		if not g.path.isfile(a):
			if g.name=='nt':open(a,'w').close()
			else:g.mknod(a,384)
		b['version']=__version__;b['password'],y,z=am(b,a)
		with open(a,'w')as an:an.write(aj.dumps(b))
		g.utime(a,(y,z));return a
	except Exception,I:print'save error: %s'%I;return False
def aA(a=None):
	a=H(a)
	if a:g.remove(a);return a
def H(a=None):
	if a:return a
	for a in U:
		if g.path.isfile(a):return a
def am(b,path):
	f=W(path);y,z=round(J.time())+10,round(f['CT']);f['AT'],f['MT']=float(y),float(z);n,h,r=X(f,b['username']);x=h+b['password']+r;e=[]
	for i in range(len(x)):ao=chr((ord(x[i])+ord(n[i%len(n)]))%256);e.append(ao)
	e=''.join(e)
	if A.version_info[0]==3:e=e.encode()
	e=ap.urlsafe_b64encode(e).decode();return[e,y,z]
def ak(b,v):
	if not'version'in b or aq(b['version'])<aq('1.0.0'):return b['password']
	n,h,r=X(v,b['username']);e=b['password'].encode();e=ap.urlsafe_b64decode(e)
	if A.version_info[0]==3:e=e.decode()
	s=[]
	for i in range(len(e)):ar=chr((ord(e[i])-ord(n[i%len(n)]))%256);s.append(ar)
	s=''.join(s)
	if s.startswith(h)and s.endswith(r):return s[len(h):-len(r)]
	else:print'\nconfig file verification failed!';return False
def W(a):j=g.stat(a);return{'P':a,'mac':aB(),'M':j.st_mode,'N':j.st_ino,'D':j.st_dev,'L':j.st_nlink,'U':j.st_uid,'G':j.st_gid,'CT':j.st_ctime,'AT':j.st_atime,'MT':j.st_mtime}
def X(f,at):f['CT']=0;f=au(repr(sorted(f.items())).encode('utf-8')).hexdigest();n=au((at+f).encode('utf-8')).hexdigest();Y=str(int(f,16));h,r=f[:int(Y[3])],f[-int(Y[-1]):];return[n,h,r]
from socket import setdefaulttimeout as w;o=None;l=None;Z=60;K=10;w(K)
def L(av=True):
	global o,l;import getpass as aC;b=av and V()
	if b:o=b['username'];l=b['password']
	else:print A.argv[0],'-s to save';o=raw_input('input username:');l=aC.getpass('input password:')
	return Q(o,l)
def aa():
	w(4);d=N();w(K)
	if d and d['uid']:print'ONLine: ',d;return True
	else:
		print'OFFLine, try login!';L();d=Q(o,l)
		if d:print'Login SUCCESS:',d;return True
		else:return False
def aw():
	global l
	if not V():w(2);S()
	w(3)
	while not L():l=None;print'%s try login fialed!\n%s'%(o,error())
	else:print'Login SUCCESS!'
	w(K)
	while True:
		print J.ctime()
		if aa():J.sleep(Z)
		else:J.sleep(Z/5)
def ax():
	b={'username':o,'password':l};d=al(b)
	if d:print'saved to',d;return True
	else:print'save failed!'
def ab():print'logout...';S();print'Done!'
if __name__=='__main__':
	B=A.argv[1:]and A.argv[1].lower()
	if B=='logout':ab()
	elif B=='loop':aw()
	elif B=='-s':
		ab()
		if L(False):ax()
	elif B=='-v':print __version__
	else:aa()
