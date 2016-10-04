#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding=utf-8
# coding:utf-8
import time
import sys


main = '''
if __name__ == "__main__":
    cmd = sys.argv[1:] and sys.argv[1].lower()

    if cmd == "logout":
        logoutAccount()
    elif cmd == "-s":
        logoutAccount()
        if getAccount(False): save()
    elif cmd == "-v":
        print __version__
    elif cmd:
        loop()
    else:
        auto()
'''


def INCLUDE(output, filename, start_tag="import", end_tag="if __name__ == '__main__'"):
    with open(filename, 'r') as gateway:
        print 'include:', filename
        if start_tag:
            for line in gateway:
                if line.startswith(start_tag):
                    output.write("\n#include form file [%s] \n" % filename)
                    output.write(line)
                    break
        for line in gateway:
            if line.startswith(end_tag):
                break
            else:
                output.write(line)

if __name__ == '__main__':
    output_file = len(sys.argv) > 1 and sys.argv[1] or 'nkuwlan.py'
    print "building to: [%s] ..." % output_file
    output = open(output_file, 'w')
    INCLUDE(output, "nkuwlan/__init__.py", start_tag=None, end_tag="__name__")
    output.write('# THIS FILE BUILD AT--- %s\n' % (time.ctime()))
    INCLUDE(output, "nkuwlan/gateway.py")
    INCLUDE(output, "nkuwlan/config.py")
    INCLUDE(output, "login.py", '# START_TAG #')
    INCLUDE(output, "logout.py", '# START_TAG #')
    output.write(main)
    output.close()
    print "Done!"
