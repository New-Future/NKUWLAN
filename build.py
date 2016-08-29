#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
#coding:utf-8
import time

#输出文件
output = open('nkulwan.py','w')

header = '''\
#!/usr/bin/python
# -*- coding: utf-8 -*-
# build at {buildtime}
'''

main = '''\
if __name__ == "__main__":
    cmd = len(sys.argv) > 1 and sys.argv[1]
    if not cmd:
        auto()
    elif cmd.lower() == "logout":
        logoutAccount()
    else:
        loop()
'''

def INCLUDE(filename,start_tag="import",end_tag="if __name__ == '__main__'"):
    with open(filename,'r') as gateway:
        print 'include:',filename
        for line in gateway:
            if line.startswith(start_tag):
                output.write(line)
                break
        for line in gateway:
            if line.startswith(end_tag):
                break
            else:
                output.write(line)

if __name__ == '__main__':

    output.write(header.format(buildtime=time.ctime()))
    INCLUDE("gateway.py")
    INCLUDE("login.py",'#START_TAG')
    INCLUDE("logout.py",'#START_TAG')
    output.write(main)
    output.close()