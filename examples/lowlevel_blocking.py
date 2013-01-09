#!/usr/bin/env python

import sys
from _ladang import *

# Directory to watch
mydir = 'mydir'

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

# For this example we'll do up to 5 get_event() call
i = 1
return_code = 0

try:
    while True:
        try:
            events = get_event(notify_fd)
        except IOError as (errno, strerror):
            print("Errno: %d" % errno)
            print("Strerror %s:" % strerror)
            return_code = 1
            break
        if events:
            for evt in events:
                print("Watch description: %d" % evt['wd'])
                print("Mask: %d" % evt['mask'])
                print("Mask descr: %s => %s" % INOTIFY_MASKS[evt['mask']])
                print("Cookie: %d" % evt['cookie'])
                print("Length: %d" % evt['len'])
                print("Name: %s" % evt['name'].strip("\0"))
                print('')
            i += 1
        if i > 5: break
finally:
    try:
        rm_watch(notify_fd, watch_fd)
        close(notify_fd)
    except:
        pass

sys.exit(return_code)
