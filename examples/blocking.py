#!/usr/bin/env python

import sys
import ladang

# Directory to watch
mydir = 'mydir'

# Initialize module
try:
    notify_fd = ladang.init()
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

ret_code = 0

try:
    while True:
        if get_event_call > 39: break
        try:
            events = ladang.get_event(notify_fd)
            get_event_call = get_event_call + 1
        except OSError as (errno, strerror):
            print("Errno: %d" % errno)
            print("Strerror %s:" % strerror)
            ret_code = 1
        for evt in events:
            print("Watch description: %d" % evt['wd'])
            print("Mask: %d" % evt['mask'])
            print("Mask descr: %s => %s" % ladang.INOTIFY_MASKS[evt['mask']])
            print("Cookie: %d" % evt['cookie'])
            print("Length: %d" % evt['len'])
            print("Name: %s" % evt['name'].strip("\0"))
finally:
    try:
        ladang.rm_watch(notify_fd, watch_fd)
        ladang.close(notify_fd)
    except:
        pass

sys.exit(ret_code)
