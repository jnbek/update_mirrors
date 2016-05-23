#!/usr/bin/env python

import os
import shlex
import subprocess
import multiprocessing

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
        'args' : '-avzz --progress --delete',
        'url'  : 'rsync.ietf.org::internet-drafts',
    },
    'ietf/rfc' : {
        'args' : '-avzz --progress',
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

max_thread = 4
lock_file  = '/tmp/update_mirrors.lock'
base_path = '/share/www/mirrors/' # need trailing /

def which(program):
    for p in os.environ['PATH'].split(':'):
        fullpath = os.path.join(p,program)
        if os.path.exists(fullpath):
            return fullpath

def build_cmd():
    cmd_list = []
    rsync_path = which("rsync")
    for path in mirrors:
        dest = str.join('',[base_path, path])
        args = str.join(chr(32), [rsync_path, mirrors[path]['args'], mirrors[path]['url'],dest])
        cmd_list.append(args)
    return cmd_list

def rsync(cmd):
    pid = os.getpid()
    print("Starting PID {0} {1}".format(pid, cmd))
    command = shlex.split(cmd)
    subprocess.call(command)
    print("Finishing PID {0} {1}".format(pid, cmd))

if __name__ == '__main__':
    if os.path.isfile(lock_file):
        print("Already running update_mirrors or stale lockfile found: Exiting")
        exit(1)
    lckf = open(lock_file, 'w')
    cmds = build_cmd()
    p = multiprocessing.Pool(max_thread)
    p.map(rsync, cmds);
    print("Main thread completed")
    lckf.close()
    os.remove(lock_file)
