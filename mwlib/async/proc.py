#! /usr/bin/env python

import os, signal
from gevent import socket, core, event

pid2status = {}

def got_signal(ev, signum):
    while 1:
        try:
            pid, st = os.waitpid(-1, os.WNOHANG)
            if pid==0:
                return
            pid2status[pid].set(st)
        except OSError:
            return

core.event(core.EV_SIGNAL|core.EV_PERSIST, signal.SIGCHLD, got_signal).add()

def run_cmd(args):
    sp = socket.socketpair()
    pid = os.fork()
    if pid==0:
        # client
        try:
            os.dup2(sp[1].fileno(), 1)
            os.dup2(sp[1].fileno(), 2)
            os.execvp(args[0], args)
        finally:
            os._exit(10)

    pid2status[pid] = event.AsyncResult()
    sp[1].close()

    chunks = []
    while 1:
        chunk = sp[0].recv(4096)
        if not chunk:
            break
        chunks.append(chunk)

    output = "".join(chunks)
    del chunks, chunk

    st = pid2status[pid].get()
    del pid2status[pid]
    return st, output
