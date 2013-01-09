#!/usr/bin/env python

import sys
import select
import ladang

# Directory to watch
mydir = 'mydir'

# Initialize module, instead of init() we user init1()
try:
    notify_fd = ladang.init1(ladang.NONBLOCK|ladang.CLOEXEC)
except OSError as (errno, strerror):
    print "Errno:", errno
    print "Strerror:", strerror
    sys.exit(1)

# Add the notification file descriptor to the watch list
# Watch for all events
try:
    watch_fd = ladang.add_watch(notify_fd, mydir, ladang.IN_ALL_EVENTS)
except OSError as (errno, strerror):
    print "Errno:", errno
    print "Strerror:", strerror
    try:
        ladang.close(notify_fd)
    except:
        pass
    sys.exit(1)

# For this example we'll do up to 40 get_event() call
get_event_call = 0

# Epoll instance
epoll_timeout = 0.1
epoll = select.epoll()

# Register notify_fd to epoll
epoll.register(notify_fd, select.EPOLLIN | select.EPOLLPRI)

# epoll error to handle
epoll_errors = select.EPOLLERR | select.EPOLLHUP

ret_code = 0

try:
    while True:
        if get_event_call > 39: break
        epoll_events = epoll.poll(epoll_timeout)
        for fileno, epoll_event in epoll_events:
            if epoll_event & epoll_errors:
                ret_code = 1
                break
            elif epoll_event & select.EPOLLIN:
                try:
                    inotify_events = ladang.get_event(notify_fd)
                    get_event_call = get_event_call + 1
                except OSError as (errno, strerror):
                    print("Errno: %d" % errno)
                    print("Strerror: %s" % strerror)
                    ret_code = 1
                    break
                for inotify_event in inotify_events:
                    print("Watch description: %d" % inotify_event['wd'])
                    print("Mask: %d" % inotify_event['mask'])
                    print("Mask descr: %s => %s" % ladang.INOTIFY_MASKS[inotify_event['mask']])
                    print("Cookie: %d" % inotify_event['cookie'])
                    print("Length: %d" % inotify_event['len'])
                    print("Name: %s" % inotify_event['name'].strip("\0"))
        if ret_code == 1: break
finally:
    try:
        ladang.rm_watch(notify_fd, watch_fd)
    except:
        pass
    epoll.unregister(notify_fd)
    epoll.close()
    ladang.close(notify_fd)

sys.exit(ret_code)
