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

max_threads = 1
queueLock = threading.Lock()
workQueue = Queue.Queue(max_threads)
threads = []
threadID = 1
#base_path = '/share/www/mirrors/' # need trailing /
base_path = '/tmp/' # need trailing /
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
    'ietf/internet-drafts' : {
        'args' : '-avz --progress --delete',
        'url'  : 'rsync.ietf.org::internet-drafts',
    },
    'ietf/rfc' : {
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
    'archhurd/repos' : {
        'args' : '-arpP --delete',
        'url'  : 'rsync.archhurd.org::repos',
    },
    'archhurd/livecd' : {
        'args' : '-arpP --delete',
        'url'  : 'rsync.archhurd.org::livecd',
    },
    'archhurd/abs' : {
        'args' : '-arpP --delete',
        'url'  : 'rsync.archhurd.org::abs',
    },
}

class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print "Starting " + self.name
        do_rsync(self.name, self.q)
        print "Exiting " + self.name

def do_rsync(threadName, q):
    print "Got in here"
    while not exitFlag:
        queueLock.acquire()
        print "After QL"
        if not workQueue.empty():
            print "Inside if not"
            data = q.get()
            queueLock.release()
            print "Thread {0} beginning: {1}".format(threadName, data) 
            print(data)
            #subprocess.call(data);
        else:
            queueLock.release()
        time.sleep(10)

def which(program):
    for p in os.environ['PATH'].split(':'):
        fullpath = "{0}/{1}".format(p,program)
        if os.path.exists(fullpath):
            return fullpath

def main():
    threadID = 1
# Create new threads
    for tName in range(max_threads):
        thread = myThread(threadID, tName, workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1

# Fill the queue
    for path in mirrors:
        dest = string.join([base_path, path],'')
        args = string.join([which("rsync"), mirrors[path]['args'], mirrors[path]['url'],dest])
        command = shlex.split(args)
        queueLock.acquire()
        workQueue.put(command)
        queueLock.release()
        print command
        

# Wait for queue to empty
    while not workQueue.empty():
        pass

# Notify threads it's time to exit
    exitFlag = 1

# Wait for all threads to complete
    for t in threads:
        t.join()
    print "Exiting Main Thread"

if __name__ == '__main__':
    main()

