#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
#coding:utf-8
import time
import sys

#header
header = '''\
#!/usr/bin/python
# -*- coding: utf-8 -*-
# build at {buildtime}
__version__ = '0.1.3'
'''

main = '''
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
'''

def INCLUDE(output,filename,start_tag="import",end_tag="if __name__ == '__main__'"):
    with open(filename,'r') as gateway:
        print 'include:',filename
        for line in gateway:
            if line.startswith(start_tag):
                output.write("\n#include form file [%s] \n"%filename)
                output.write(line)
                break
        for line in gateway:
            if line.startswith(end_tag):
                break
            else:
                output.write(line)

if __name__ == '__main__':
    output_file=  len(sys.argv) > 1 and sys.argv[1] or 'nkuwlan.py'
    print "building to: [%s] ..."%output_file
    output= open(output_file,'w')
    output.write(header.format(buildtime=time.ctime()))
    INCLUDE(output,"gateway.py")
    INCLUDE(output,"config.py")
    INCLUDE(output,"login.py",'#START_TAG')
    INCLUDE(output,"logout.py",'#START_TAG')
    output.write(main)
    output.close()
    print "Done!"