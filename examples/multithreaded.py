#!/usr/bin/env python

import sys
import threading
import ladang

def watch_worker(notify_fd):
    get_event_call = 0
    while True:
        if get_event_call > 2: break
        lock.acquire()
        try:
            events = ladang.get_event(notify_fd)
            if len(events) > 0: get_event_call = get_event_call + 1
        except OSError as (errno, strerror):
            print("Errno: %d" % errno)
            print("Strierror %s:" % strerror)
            raise
        if events:
            print(threading.currentThread().getName())
            for evt in events:
                print("Watch description: %d" % evt['wd'])
                print("Mask: %d" % evt['mask'])
                print("Mask descr: %s => %s" % ladang.INOTIFY_MASKS[evt['mask']])
                print("Cookie: %d" % evt['cookie'])
                print("Length: %d" % evt['len'])
                print("Name: %s" % evt['name'].strip("\0"))
                print("")
        lock.release()

if __name__ == '__main__':
    ret_code = 0
    mydir = 'mydir'
    lock = threading.Lock()

    # Initialize module
    try:
        notify_fd = ladang.init()
        print "fd:", notify_fd
    except OSError as (errno, strerror):
        print "Errno:", errno
        print "Strerror:", strerror
        sys.exit(1)

    # Add the notification file descriptor to the watch list
    # Watch for all events
    try:
        watch_fd = ladang.add_watch(notify_fd, mydir, ladang.IN_ALL_EVENTS)
        print "wd:", watch_fd
    except OSError as (errno, strerror):
        print "Errno:", errno
        print "Strerror:", strerror
        try:
            ladang.close(notify_fd)
        except:
            pass
        sys.exit(1)

    args = notify_fd,

    try:
        # 2 threads
        threads = []
        for i in range(2):
            t = threading.Thread(target=watch_worker, args=args)
            threads.append(t)
            t.start()
    finally:
        for i in range(2):
            threads[i].join()
        try:
            ladang.rm_watch(notify_fd, watch_fd)
            ladang.close(notify_fd)
        except:
            pass

    sys.exit(ret_code)
