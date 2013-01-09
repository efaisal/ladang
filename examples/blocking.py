#!/usr/bin/env python

import sys
from ladang import *

# Directory to watch
mydir = 'mydir'

# Initialize module
inotify = Ladang()

# Register a file or directory to watch
# Watch for all events, if you wish to watch add the mask parameter
inotify.watch(mydir)

# For this example we'll capture up to 5 events
i = 1
while True:
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

# We no longer interested to monitor anything, lets tell the kernel
inotify.close()

sys.exit(0)
