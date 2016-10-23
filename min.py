#!/usr/bin/env python
# -*- coding: utf-8 -*-
__version__='2.0.0';__author__='New Future';import urllib;import urllib2 as ad;C=['http://202.113.18.106'];at='/';Z=':801/eportal/?c=ACSetting&a=Login';aa=':801/eportal/?c=ACSetting&a=Logout';L=None
def M(w=None):
 if type(w)is str:D=[w]
 elif w:D=w
 else:D=C
 for c in D:
  o=E(c)
  if o:
   N=find(o,"flow='");O=find(o,"fee='");d={'fee':O and int(O),'flow':N and int(N)/1024,'uid':find(o,"uid='"),'ipv4':find(o,"v4ip='")}
   if d['uid']:return d
def P(ab,x):
 q={'DDDDD':ab,'upass':x};q=urllib.urlencode(q)
 for c in C:
  F=c+Z;E(F,q);d=M(c)
  if d and d['uid']:return d
def Q():
 for c in C:E(c+aa)
def error():return L
def find(r,g,ac="'"):
 p=r.find(g)
 if p>0:r=r[len(g)+p:];G=r[:r.find(ac)];return G.strip()
def E(F,q=None):
 try:ad.getproxies=lambda:{};return ad.urlopen(F,q).read()
 except Exception,s:L=s;return None
import base64 as ak;import json as af;import os as f;import sys as A;import time as I;from distutils.version import StrictVersion as al;from hashlib import sha512 as ao;from uuid import getnode as av;_a=f.path.expanduser('~');R=[_a+'/.nkuwlan/conf.json',_a+'/.nkuwlan.json','/etc/nkuwlan/conf.json']
def S(a=None):
 a=H(a)
 if a:
  try:
   t=T(a)
   with open(a,'r')as ae:
    b=af.load(ae);b['password']=ag(b,t)
    if not b['password']:return False
   f.utime(a,(t['AT'],t['MT']));return b
  except Exception,s:print'load config failed: %s'%s;return False
def ah(b,a=None):
 a=H(a)or R[0];dir=f.path.dirname(a)
 try:
  if not f.path.exists(dir):f.mkdir(dir,448)
  if not f.path.isfile(a):
   if f.name=='nt':open(a,'w').close()
   else:f.mknod(a,384)
  b['version']=__version__;b['password'],y,z=ai(b,a)
  with open(a,'w')as G:G.write(af.dumps(b))
  f.utime(a,(y,z));return a
 except Exception,s:print'save error: %s'%s;return False
def au(a=None):
 a=H(a)
 if a:f.remove(a);return a
def H(a=None):
 if a:return a
 for a in R:
  if f.path.isfile(a):return a
def ai(b,path):
 c=T(path);y,z=round(I.time())+10,round(c['CT']);c['AT'],c['MT']=float(y),float(z);j,g,l=U(c,b['username']);x=g+b['password']+l;e=[]
 for u in range(len(x)):aj=chr((ord(x[u])+ord(j[u%len(j)]))%256);e.append(aj)
 e=''.join(e)
 if A.version_info[0]==3:e=e.encode()
 e=ak.urlsafe_b64encode(e).decode();return[e,y,z]
def ag(b,t):
 if not'version'in b or al(b['version'])<al('1.0.0'):return b['password']
 j,g,l=U(t,b['username']);e=b['password'].encode();e=ak.urlsafe_b64decode(e)
 if A.version_info[0]==3:e=e.decode()
 n=[]
 for u in range(len(e)):am=chr((ord(e[u])-ord(j[u%len(j)]))%256);n.append(am)
 n=''.join(n)
 if n.startswith(g)and n.endswith(l):return n[len(g):-len(l)]
 else:print'\nconfig file verification failed!';return False
def T(a):h=f.stat(a);return{'P':a,'mac':av(),'M':h.st_mode,'N':h.st_ino,'D':h.st_dev,'L':h.st_nlink,'U':h.st_uid,'G':h.st_gid,'CT':h.st_ctime,'AT':h.st_atime,'MT':h.st_mtime}
def U(c,an):c['CT']=0;c=ao(repr(sorted(c.items())).encode('utf-8')).hexdigest();j=ao((an+c).encode('utf-8')).hexdigest();V=str(int(c,16));g,l=c[:int(V[3])],c[-int(V[-1]):];return[j,g,l]
from socket import setdefaulttimeout as v;k=None;i=None;W=60;J=10;v(J)
def K(ap=True):
 global k,i;import getpass as aw;b=ap and S()
 if b:k=b['username'];i=b['password']
 else:print A.argv[0],'-s to save';k=raw_input('input username:');i=aw.getpass('input password:')
 return P(k,i)
def X():
 v(4);d=M();v(J)
 if d and d['uid']:print'ONLine: ',d;return True
 else:
  print'OFFLine, try login!';K();d=P(k,i)
  if d:print'Login SUCCESS:',d;return True
  else:return False
def aq():
 global i
 if not S():v(2);Q()
 v(3)
 while not K():i=None;print'%s try login fialed!\n%s'%(k,error())
 else:print'Login SUCCESS!'
 v(J)
 while True:
  print I.ctime()
  if X():I.sleep(W)
  else:I.sleep(W/5)
def ar():
 b={'username':k,'password':i};d=ah(b)
 if d:print'saved to',d;return True
 else:print'save failed!'
def Y():print'logout...';Q();print'Done!'
if __name__=='__main__':
 B=A.argv[1:]and A.argv[1].lower()
 if B=='logout':Y()
 elif B=='loop':aq()
 elif B=='-s':
  Y()
  if K(False):ar()
 elif B=='-v':print __version__
 else:X()
