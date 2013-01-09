#!/usr/bin/env python

import sys
import select
from ladang import *

# Directory to watch
mydir = 'mydir'

# Initialize module, with non-blocking flag
inotify = Ladang(NONBLOCK|CLOEXEC)

# Register a file or directory to watch
# Watch for all events, if you wish to watch add the mask parameter
inotify.watch(mydir)

# We're going to use epoll - level-triggered
# Then register the inotify event queue file descriptor to epoll
epoll = select.epoll()
epoll.register(inotify.get_fd(), select.EPOLLIN | select.EPOLLPRI)
epoll_errors = select.EPOLLERR | select.EPOLLHUP

# For this example we'll capture up to 5 events
i = 1
while True:
    epoll_events = epoll.poll(0.1)
    for fileno, epoll_event in epoll_events:
        if epoll_event & epoll_errors:
            return_code = 1
        elif epoll_event & select.EPOLLIN:
            events = inotify.get_event()
            if events:
                for evt in events:
                    print("Watched path: %s" % evt['wd'])
                    print("Mask: %d" % evt['mask'])
                    print("Mask descr: %s => %s" % INOTIFY_MASKS[evt['mask']])
                    print("Cookie: %d" % evt['cookie'])
                    print("Name: %s" % evt['name'])
                print('')
                i += 1
    if i > 5: break

# Stop watching the registered dir
inotify.unwatch(mydir)

# Doing epoll cleanup stuffs
epoll.unregister(inotify.get_fd())
epoll.close()

# We no longer interested to monitor anything, lets tell the kernel
inotify.close()

sys.exit(0)
