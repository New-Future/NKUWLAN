#!/usr/bin/env python
# -*- coding: utf-8 -*-
__version__='1.2.0';__author__='New Future';import urllib;import urllib2 as ac;A=['http://202.113.18.110','http://202.113.18.210'];ap='/';Y=':801/eportal/?c=ACSetting&a=Login';Z=':801/eportal/?c=ACSetting&a=Logout';K=None
def L(v=None):
 if type(v)is str:B=[v]
 elif v:B=v
 else:B=A
 for c in B:
  o=C(c)
  if o:
   M=find(o,"flow='");N=find(o,"fee='");d={'fee':N and int(N),'flow':M and int(M)/1024,'uid':find(o,"uid='"),'ipv4':find(o,"v4ip='")}
   if d['uid']:return d
def O(aa,w):
 q={'DDDDD':aa,'upass':w};q=urllib.urlencode(q)
 for c in A:
  D=c+Y;C(D,q);d=L(c)
  if d and d['uid']:return d
def P():
 for c in A:C(c+Z)
def error():return K
def find(r,g,ab="'"):
 p=r.find(g)
 if p>0:r=r[len(g)+p:];E=r[:r.find(ab)];return E.strip()
def C(D,q=None):
 try:ac.getproxies=lambda:{};return ac.urlopen(D,q).read()
 except Exception,s:K=s;return None
import base64 as ah;import json as ae;import os as f;import sys as H;import time as G;from distutils.version import StrictVersion as ai;from hashlib import sha512 as al;from uuid import getnode as ar;_a=f.path.expanduser('~');Q=[_a+'/.nkuwlan/conf.json',_a+'/.nkuwlan.json','/etc/nkuwlan/conf.json']
def R(a=None):
 a=F(a)
 if a:
  try:
   with open(a,'r')as ad:
    b=ae.load(ad)
    if'version'in b:
     b['password']=decode(b,a)
     if not b['password']:return False
    return b
  except Exception,s:print'load config failed: %s'%s;return False
def af(b,a=None):
 a=F(a)or Q[0];dir=f.path.dirname(a)
 try:
  if not f.path.exists(dir):f.mkdir(dir,448)
  if not f.path.isfile(a):
   if f.name=='nt':open(a,'w').close()
   else:f.mknod(a,384)
  b['version']=__version__;b['password'],x,y=encode(b,a)
  with open(a,'w')as E:E.write(ae.dumps(b))
  f.utime(a,(x,y));return a
 except Exception,s:print'save error: %s'%s;return False
def aq(a=None):
 a=F(a)
 if a:f.remove(a);return a
def F(a=None):
 if a:return a
 for a in Q:
  if f.path.isfile(a):return a
def encode(b,path):
 c=S(path);x,y=round(G.time())+10,round(c['CT']);c['AT'],c['MT']=float(x),float(y);j,g,l=T(c,b['username']);w=g+b['password']+l;e=[]
 for t in range(len(w)):ag=chr((ord(w[t])+ord(j[t%len(j)]))%256);e.append(ag)
 e=''.join(e)
 if H.version_info[0]==3:e=e.encode()
 e=ah.urlsafe_b64encode(e).decode();return[e,x,y]
def decode(b,path):
 if ai(b['version'])<ai('1.0.0'):return b['password']
 c=S(path);j,g,l=T(c,b['username']);e=b['password'].encode();e=ah.urlsafe_b64decode(e)
 if H.version_info[0]==3:e=e.decode()
 n=[]
 for t in range(len(e)):aj=chr((ord(e[t])-ord(j[t%len(j)]))%256);n.append(aj)
 n=''.join(n)
 if n.startswith(g)and n.endswith(l):return n[len(g):-len(l)]
 else:print'\nconfig file verification failed!';return False
def S(a):h=f.stat(a);return{'P':a,'mac':ar(),'M':h.st_mode,'N':h.st_ino,'D':h.st_dev,'L':h.st_nlink,'U':h.st_uid,'G':h.st_gid,'CT':h.st_ctime,'AT':h.st_atime,'MT':h.st_mtime}
def T(c,ak):c['CT']=0;c=al(repr(sorted(c.items())).encode('utf-8')).hexdigest();j=al((ak+c).encode('utf-8')).hexdigest();U=str(int(c,16));g,l=c[:int(U[3])],c[-int(U[-1]):];return[j,g,l]
from socket import setdefaulttimeout as u;k=None;i=None;V=60;I=10;u(I)
def J(am=True):
 global k,i;import getpass as at;b=am and R()
 if b:k=b['username'];i=b['password']
 else:k=raw_input('input username:');i=at.getpass('input password:')
 return O(k,i)
def W():
 u(4);d=L();u(I)
 if d and d['uid']:print'ONLine: ',d;return True
 else:
  print'OFFLine, try login!';J();d=O(k,i)
  if d:print'Login SUCCESS:',d;return True
  else:return False
def an():
 global i
 if not R():u(2);P()
 u(3)
 while not J():i=None;print'%s try login fialed!\n%s'%(k,error())
 else:print'Login SUCCESS!'
 u(I)
 while True:
  print G.ctime()
  if W():G.sleep(V)
  else:G.sleep(V/5)
def ao():
 b={'username':k,'password':i};d=af(b)
 if d:print'saved to '+d;return True
 else:print'save failed!'
def X():print'wait...';P();print'\nlogout success!'
if __name__=='__main__':
 z=H.argv[1:]and H.argv[1].lower()
 if z=='logout':X()
 elif z=='loop':an()
 elif z=='-s':
  X()
  if J(False):ao()
 elif z=='-v':print __version__
 else:W()
