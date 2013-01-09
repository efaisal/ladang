#!/usr/bin/env python

import sys
import threading
from _ladang import *

def worker(notify_fd, lock):
    i = 1
    while True:
        lock.acquire()
        try:
            events = get_event(notify_fd)
        except IOError as (errno, strerror):
            print("Errno: %d" % errno)
            print("Strierror %s:" % strerror)
            raise
        if events:
            print(threading.currentThread().getName())
            for evt in events:
                print("Watch description: %d" % evt['wd'])
                print("Mask: %d" % evt['mask'])
                print("Mask descr: %s => %s" % INOTIFY_MASKS[evt['mask']])
                print("Cookie: %d" % evt['cookie'])
                print("Length: %d" % evt['len'])
                print("Name: %s" % evt['name'].strip("\0"))
                print('')
            i += 1
        lock.release()
        if i > 2: break

if __name__ == '__main__':
    mydir = 'mydir'
    lock = threading.Lock()

    # Initialize module
    try:
        notify_fd = init()
    except IOError as (errno, strerror):
        print "Errno:", errno
        print "Strerror:", strerror
        sys.exit(1)

    # Add the notification file descriptor to the watch list
    # Watch for all events
    try:
        watch_fd = add_watch(notify_fd, mydir, IN_ALL_EVENTS)
    except IOError as (errno, strerror):
        print "Errno:", errno
        print "Strerror:", strerror
        try:
            close(notify_fd)
        except:
            pass
        sys.exit(1)

    # We test with 2 threads
    num_of_threads = 2
    try:
        threads = []
        for i in range(num_of_threads):
            t = threading.Thread(target=worker, args=[notify_fd, lock])
            threads.append(t)
            t.start()
    finally:
        for i in range(num_of_threads):
            threads[i].join()
        try:
            rm_watch(notify_fd, watch_fd)
            close(notify_fd)
        except:
            pass

    sys.exit(0)
