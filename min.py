#!/usr/bin/env python
# -*- coding: utf-8 -*-
__version__='1.1.0';__author__='New Future';import urllib2 as af;import urllib;A=['http://202.113.18.110','http://202.113.18.210'];av='/';Z=':801/eportal/?c=ACSetting&a=Login';aa=':801/eportal/?c=ACSetting&a=Logout';B=None
def N(u=None):
 if u==None:C=A
 elif type(u)is str:C=[u]
 else:C=u
 d=None
 for c in C:
  n=D(c)
  if n==None:continue
  else:
   O=find(n,"uid='");o=find(n,"flow='");o=int(o)if o else 0;E=find(n,"fee='");E=int(E)if o else 0;ab=find(n,"v4ip='");d={'uid':O,'fee':E,'flow':o/1024,'ipv4':ab}
   if O!=None:return d
   else:continue
 return d
def P(ac,v):
 p={'DDDDD':ac,'upass':v};p=urllib.urlencode(p)
 for c in A:
  F=c+Z;D(F,p);d=N(c)
  if d!=None and d['uid']!=None:return d
def Q():
 for c in A:D(c+aa)
def ad():return B
def find(q,i,ae="'"):
 R=q.find(i)
 if R>0:q=q[len(i)+R:];k=q.find(ae);G=q[:k];return G.strip()
def D(F,p=None):
 global B
 try:af.getproxies=lambda:{};ag=af.urlopen(F,p);return ag.read()
 except Exception,r:B=r;return None
import os as f;import json as ai;import sys as K;import base64 as al;import hashlib as aq;import uuid;import time as I;from distutils.version import StrictVersion as am;S=[f.path.expanduser('~')+'/.nkuwlan/conf.json',f.path.expanduser('~')+'/.nkuwlan.json','/etc/nkuwlan/conf.json']
def T(a=None):
 a=H(a)
 if a:
  try:
   with open(a,'r')as ah:
    b=ai.load(ah)
    if'version'in b:
     b['password']=decode(b,a)
     if not b['password']:return False
    return b
  except Exception,r:print'load config failed: %s'%r;return False
def aj(b,a=None):
 a=H(a)or S[0];dir=f.path.dirname(a)
 try:
  if not f.path.exists(dir):f.mkdir(dir,448)
  if not f.path.isfile(a):
   if f.name=='nt':open(a,'w').close()
   else:f.mknod(a,384)
  b['version']=__version__;b['password'],w,x=encode(b,a)
  with open(a,'w')as G:G.write(ai.dumps(b))
  f.utime(a,(w,x));return a
 except Exception,r:print'save error: %s'%r;return False
def aw(a=None):
 a=H(a)
 if a:f.remove(a);return a
def H(a=None):
 if a:return a
 for a in S:
  if f.path.isfile(a):return a
def encode(b,path):
 c=U(path);w,x=round(I.time())+10,round(c['ctime']);c['atime'],c['mtime']=float(w),float(x);l,i,k=V(c,b['username']);v=i+b['password']+k;e=[]
 for s in range(len(v)):J=l[s%len(l)];ak=chr((ord(v[s])+ord(J))%256);e.append(ak)
 e=''.join(e)
 if K.version_info[0]==3:e=e.encode()
 e=al.urlsafe_b64encode(e).decode();return[e,w,x]
def decode(b,path):
 if am(b['version'])<am('1.0.0'):return b['password']
 c=U(path);l,i,k=V(c,b['username']);e=b['password'].encode();e=al.urlsafe_b64decode(e)
 if K.version_info[0]==3:e=e.decode()
 m=[]
 for s in range(len(e)):J=l[s%len(l)];an=chr((256+ord(e[s])-ord(J))%256);m.append(an)
 m=''.join(m)
 if m.startswith(i)and m.endswith(k):return m[len(i):-len(k)]
 else:print'\nThe config file verification failed\xef\xbc\x81\n\xe9\x85\x8d\xe7\xbd\xae\xe6\x96\x87\xe4\xbb\xb6\xe6\xa0\xa1\xe9\xaa\x8c\xe5\xa4\xb1\xe8\xb4\xa5!\n\xe6\x82\xa8\xe7\x9a\x84\xe9\x85\x8d\xe7\xbd\xae\xe6\x96\x87\xe4\xbb\xb6\xe5\x8f\xaf\xe8\x83\xbd\xe5\xb7\xb2\xe8\xa2\xab\xe4\xba\xba\xe5\x81\xb7\xe7\xaa\xa5\xe6\x88\x96\xe4\xbf\xae\xe6\x94\xb9!(\xe6\x94\xbe\xe5\xbf\x83\xe5\xaf\x86\xe7\xa0\x81\xe5\xb7\xb2\xe7\x89\xb9\xe6\xae\x8a\xe5\x8a\xa0\xe5\xaf\x86)\nWARN:\xe4\xb8\xba\xe4\xba\x86\xe4\xbf\x9d\xe8\xaf\x81\xe8\xb4\xa6\xe6\x88\xb7\xe5\xae\x89\xe5\x85\xa8,\xe4\xbf\xae\xe6\x94\xb9\xe6\x88\x96\xe8\x80\x85\xe7\xa7\xbb\xe5\x8a\xa8\xe9\x85\x8d\xe7\xbd\xae\xe6\x96\x87\xe4\xbb\xb6\xe5\x9d\x87\xe4\xbc\x9a\xe5\xaf\xbc\xe8\x87\xb4\xe5\xaf\x86\xe9\x92\xa5\xe5\xa4\xb1\xe6\x95\x88!';return False
def U(a):import uuid;j=f.stat(a);ao={'path':a,'mac':uuid.getnode(),'mode':j.st_mode,'inode':j.st_ino,'device':j.st_dev,'nlink':j.st_nlink,'user':j.st_uid,'group':j.st_gid,'ctime':j.st_ctime,'atime':j.st_atime,'mtime':j.st_mtime};return ao
def V(c,ap):c['ctime']=0;c=aq.md5(repr(sorted(c.items())).encode('utf-8')).hexdigest();l=aq.sha512((ap+c).encode('utf-8')).hexdigest();W=str(int(c,16));i,k=c[:int(W[3])],c[-int(W[-1]):];return[l,i,k]
import sys as K;import socket as t;g=None;h=None;L=60;y=10;t.setdefaulttimeout(y)
def M(ar=True):
 import getpass as ax;global g,h;b=ar and T()
 if b:g=b['username'];h=b['password']
 g=g or raw_input('input username [ \xe5\xad\xa6\xe5\x8f\xb7\xe6\x88\x96\xe8\xb4\xa6\xe5\x8f\xb7 ]:');h=h or ax.getpass('input password [ \xe6\xa0\xa1\xe5\x9b\xad\xe7\xbd\x91\xe5\xaf\x86\xe7\xa0\x81 ]:');return P(g,h)
def X():
 global g,h;t.setdefaulttimeout(4);d=N();t.setdefaulttimeout(y)
 if d and d['uid']:print'ONLine: ',d;return True
 else:
  print'OFFLine, try login!';M();d=P(g,h)
  if d:print'Login SUCCESS:',d;return True
  else:return False
def at():
 import time as I;global L,y,g,h
 if not T():t.setdefaulttimeout(2);Q()
 t.setdefaulttimeout(3)
 while not M():h=None;print'%s try login fialed!'%g;print ad()
 else:print'Login SUCCESS! [ \xe7\x99\xbb\xe5\xbd\x95\xe6\x88\x90\xe5\x8a\x9f! ]'
 t.setdefaulttimeout(y)
 while True:
  print I.ctime()
  if X():I.sleep(L)
  else:I.sleep(L/5)
def au():
 b={'version':__version__,'username':g,'password':h};d=aj(b)
 if d:print'saved to %s'%d;return True
 else:print'save failed!';return False
def Y():print'waiting...';Q();print'logout success![ \xe6\xa0\xa1\xe5\x9b\xad\xe7\xbd\x91\xe5\xb7\xb2\xe6\xb3\xa8\xe9\x94\x80 ]'
if __name__=='__main__':
 z=len(K.argv)>1and K.argv[1].lower()
 if not z:X()
 elif z=='logout':Y()
 elif z=='-s':
  Y()
  if M(False):au()
 elif z=='-v':print'NKUWLAN (python) verison :',__version__
 else:at()
