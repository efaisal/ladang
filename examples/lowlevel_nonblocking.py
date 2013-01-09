#!/usr/bin/env python

import sys
import select
from _ladang import *

# Directory to watch
mydir = 'mydir'

# Initialize module, instead of init() we user init1()
try:
    notify_fd = init1(NONBLOCK|CLOEXEC)
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

# Epoll instance
epoll_timeout = 0.1
epoll = select.epoll()
# Register notify_fd to epoll
epoll.register(notify_fd, select.EPOLLIN | select.EPOLLPRI)
# epoll error to handle
epoll_errors = select.EPOLLERR | select.EPOLLHUP

return_code = 0

try:
    i = 1
    while True:
        epoll_events = epoll.poll(epoll_timeout)
        for fileno, epoll_event in epoll_events:
            if epoll_event & epoll_errors:
                return_code = 1
                break
            elif epoll_event & select.EPOLLIN:
                try:
                    inotify_events = get_event(notify_fd)
                except IOError as (errno, strerror):
                    print("Errno: %d" % errno)
                    print("Strerror: %s" % strerror)
                    return_code = 1
                    break
                if inotify_events:
                    for inotify_event in inotify_events:
                        print("Watch description: %d" % inotify_event['wd'])
                        print("Mask: %d" % inotify_event['mask'])
                        print("Mask descr: %s => %s" % INOTIFY_MASKS[inotify_event['mask']])
                        print("Cookie: %d" % inotify_event['cookie'])
                        print("Length: %d" % inotify_event['len'])
                        print("Name: %s" % inotify_event['name'].strip("\0"))
                    print('')
                    i += 1
        if i > 5: break
finally:
    try:
        rm_watch(notify_fd, watch_fd)
    except:
        pass
    epoll.unregister(notify_fd)
    epoll.close()
    close(notify_fd)

sys.exit(return_code)
