#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import shlex
import Queue
import string
import threading
import subprocess

exitFlag = 0

base_path = '/share/www/mirrors/' # need trailing /
mirrors = {
    'pacbsd' : {
        'args' : '-azzrpP --delete',
        'url'  : 'rsync.pacbsd.org::Repository',
    },
    'cpan' : {
        'args' : '-arpP --delete',
        'url'  : 'cpan-rsync.perl.org::CPAN',
    },
    'gnu' : {
        'args' : '-rltpHS --progress --delete-excluded',
        'url'  : 'rsync://mirrors.ocf.berkeley.edu/gnu/',
    },
    'nongnu' : {
        'args' : '-rltpHS --progress --delete-excluded',
        'url'  : 'rsync://dl.sv.gnu.org/releases/',
    },
    'opencsw' : {
        'args' : '-aH --progress --delete',
        'url'  : 'rsync://rsync.opencsw.org/opencsw/',
    },
    'internet-drafts' : {
        'args' : '-avz --progress --delete',
        'url'  : 'rsync.ietf.org::internet-drafts',
    },
    'rfc' : {
        'args' : '-avz --progress',
        'url'  : 'rsync.ietf.org::rfc',
    },
    'openindiana/dlc': {
        'args' : '-av --delete --progress',
        'url'  : 'dlc-origin.openindiana.org::dlc',
    },
    'openindiana/pkg/dev' : {
        'args' : '-av --delete --progress',
        'url'  : 'pkg-origin.openindiana.org::pkgdepot-dev',
    },
}

archhurd_mirrors = {
    'repos' : {
        'args' : '-arpP --delete',
        'url'  : 'rsync.archhurd.org::repos',
    },
    'livecd' : {
        'args' : '-arpP --delete',
        'url'  : 'rsync.archhurd.org::livecd',
    },
    'abs' : {
        'args' : '-arpP --delete',
        'url'  : 'rsync.archhurd.org::abs',
    },
}

class myThread (threading.Thread):

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print "Starting " + self.name
        print_time(self.name, self.counter, 5)
        print "Exiting " + self.name

def do_rsync(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print "%s processing %s" % (threadName, data)
        else:
            queueLock.release()
        time.sleep(1)


def main():
    for path in mirrors:
        dest = string.join([base_path, path],'')
        args = string.join([which("rsync"), mirrors[path]['args'], mirrors[path]['url'],dest])
        command = shlex.split(args)
        print command

# main

def which(program):
    for p in os.environ['PATH'].split(':'):
        fullpath = "{0}/{1}".format(p,program)
        if os.path.exists(fullpath):
            return fullpath

if __name__ == '__main__':
    main()

