#!/usr/bin/env python
# coding:utf-8

import subprocess
import sys
import time
import os
from sys import platform
from notificate import notificate

if __name__ == '__main__':
    # read configure file get target
    target = None
    configpath = os.path.join(os.path.dirname(__file__), 'configure.ini')
    with open(configpath) as f:
        for line in f:
            if line.startswith('target'):
                target = line.split('=')[1].strip()
    if not target:
        print 'Not find target!'
        sys.exit()

    if 'linux' in platform:
        args = ['ps', 'ux']
    elif platform == 'win32':
        args = 'tasklist'
    flag = True
    while True:
        p = subprocess.Popen(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if target not in out and flag:
            # notifacate
            subject = 'Warning: Program exit'
            message = '%s has exited' % target
            notificate.notificate(subject, message)
            flag = False
        if target in out:
            flag = True
        time.sleep(10)
