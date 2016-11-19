#!/usr/bin/env python
# -*- coding: utf-8 -*-
__version__='2.0.0';__author__='New Future';import base64 as R;import json as L;import os as e;import sys as u;import time as y;from distutils.version import StrictVersion as S;from hashlib import sha512 as V;from uuid import getnode as ac;_a=e.path.expanduser('~');B=[_a+'/.nkuwlan/conf.json',_a+'/.nkuwlan.json','/etc/nkuwlan/conf.json']
def C(a=None):
 a=w(a)
 if a:
  try:
   o=D(a)
   with open(a,'r')as K:
    b=L.load(K);b['password']=M(b,o)
    if not b['password']:return False
   e.utime(a,(o['AT'],o['MT']));return b
  except Exception,x:print'load config failed: %s'%x;return False
def N(b,a=None):
 a=w(a)or B[0];dir=e.path.dirname(a)
 try:
  if not e.path.exists(dir):e.mkdir(dir,448)
  if not e.path.isfile(a):
   if e.name=='nt':open(a,'w').close()
   else:e.mknod(a,384)
  b['version']=__version__;b['password'],s,t=O(b,a)
  with open(a,'w')as P:P.write(L.dumps(b))
  e.utime(a,(s,t));return a
 except Exception,x:print'save error: %s'%x;return False
def ab(a=None):
 a=w(a)
 if a:e.remove(a);return a
def w(a=None):
 if a:return a
 for a in B:
  if e.path.isfile(a):return a
def O(b,path):
 d=D(path);s,t=round(y.time())+10,round(d['CT']);d['AT'],d['MT']=float(s),float(t);i,k,l=E(d,b['username']);F=k+b['password']+l;c=[]
 for q in range(len(F)):Q=chr((ord(F[q])+ord(i[q%len(i)]))%256);c.append(Q)
 c=''.join(c)
 if u.version_info[0]==3:c=c.encode()
 c=R.urlsafe_b64encode(c).decode();return[c,s,t]
def M(b,o):
 if not'version'in b or S(b['version'])<S('1.0.0'):return b['password']
 i,k,l=E(o,b['username']);c=b['password'].encode();c=R.urlsafe_b64decode(c)
 if u.version_info[0]==3:c=c.decode()
 n=[]
 for q in range(len(c)):T=chr((ord(c[q])-ord(i[q%len(i)]))%256);n.append(T)
 n=''.join(n)
 if n.startswith(k)and n.endswith(l):return n[len(k):-len(l)]
 else:print'\nconfig file verification failed!';return False
def D(a):f=e.stat(a);return{'P':a,'mac':ac(),'M':f.st_mode,'N':f.st_ino,'D':f.st_dev,'L':f.st_nlink,'U':f.st_uid,'G':f.st_gid,'CT':f.st_ctime,'AT':f.st_atime,'MT':f.st_mtime}
def E(d,U):d['CT']=0;d=V(repr(sorted(d.items())).encode('utf-8')).hexdigest();i=V((U+d).encode('utf-8')).hexdigest();G=str(int(d,16));k,l=d[:int(G[3])],d[-int(G[-1]):];return[i,k,l]
from socket import setdefaulttimeout as r;j=None;h=None;H=60;z=10;r(z)
def A(W=True):
 global j,h;import getpass as ad;b=W and C()
 if b:j=b['username'];h=b['password']
 else:print u.argv[0],'-s to save';j=raw_input('input username:');h=ad.getpass('input password:')
 return X(j,h)
def I():
 r(4);g=ae();r(z)
 if g and g['uid']:print'ONLine: ',g;return True
 else:
  print'OFFLine, try login!';A();g=X(j,h)
  if g:print'Login SUCCESS:',g;return True
  else:return False
def Y():
 global h
 if not C():r(2);Z()
 r(3)
 while not A():h=None;print'%s try login fialed!\n%s'%(j,error())
 else:print'Login SUCCESS!'
 r(z)
 while True:
  print y.ctime()
  if I():y.sleep(H)
  else:y.sleep(H/5)
def aa():
 b={'username':j,'password':h};g=N(b)
 if g:print'saved to',g;return True
 else:print'save failed!'
def J():print'logout...';Z();print'Done!'
if __name__=='__main__':
 v=u.argv[1:]and u.argv[1].lower()
 if v=='logout':J()
 elif v=='loop':Y()
 elif v=='-s':
  J()
  if A(False):aa()
 elif v=='-v':print __version__
 else:I()
