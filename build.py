#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding:utf-8
import time
import sys


MAIN = '''
if __name__ == "__main__":
    cmd = sys.argv[1:] and sys.argv[1].lower()

    if cmd == "logout":
        logoutAccount()
    elif cmd == "loop":
        loop()
    elif cmd == "-s":
        logoutAccount()
        if getAccount(False): save()
    elif cmd == "-v":
        print __version__
    else:
        auto()
'''


def include(output, filename, start_tag="import", end_tag="if __name__ == '__main__'"):
    """include python file
    """
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


def build(output_file):
    """
    build to
    """
    print "building to: [%s] ..." % output_file
    output = open(output_file, 'w')
    include(output, "nkuwlan/__init__.py", start_tag=None, end_tag="__name__")
    output.write('# THIS FILE AUTO BUILD AT--- %s ---\n' % (time.ctime()))
    include(output, "nkuwlan/gateway.py", 'try:')
    include(output, "nkuwlan/config.py")
    include(output, "login.py", '# START_TAG #')
    include(output, "logout.py", '# START_TAG #')
    output.write(MAIN)
    output.close()
    print "Done!"


def tabs(source, output):
    """space to tabs"""
    with open(source) as input_file:
        lines = input_file.readlines()
    with open(output, 'w') as output_file:
        del lines[1]
        for line in lines:
            if not line:
                break
            for i in xrange(len(line)):
                if line[i] == " ":
                    output_file.write("\t")
                else:
                    output_file.write(line[i:])
                    break

        # output_file.writelines(lines)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        build('nkuwlan.py')
    elif len(sys.argv) == 2:
        build(sys.argv[1])
    else:
        tabs(sys.argv[1], sys.argv[2])
