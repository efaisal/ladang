#!/usr/bin/env python

import sys
import threading
from ladang import *

# Worker thread
def worker(inotify, lock):
    # For this example we'll capture up to 2 events per thread
    i = 1
    while True:
        lock.acquire()
        events = inotify.get_event()
        if events:
            print(threading.currentThread().getName())
            for evt in events:
                print("Watched path: %s" % evt['wd'])
                print("Mask: %d" % evt['mask'])
                print("Mask descr: %s => %s" % INOTIFY_MASKS[evt['mask']])
                print("Cookie: %d" % evt['cookie'])
                print("Name: %s" % evt['name'])
            print('')
            i += 1
        lock.release()
        if i > 2: break

if __name__ == '__main__':
    # Lock
    lock = threading.Lock()

    # Directory to watch
    mydir = 'mydir'

    # Initialize module
    inotify = Ladang()

    # Register a file or directory to watch
    # Watch for all events, if you wish to watch add the mask parameter
    inotify.watch(mydir)

    # Lets have 2 child threads
    num_of_threads = 2
    try:
        threads = []
        for i in range(num_of_threads):
            t = threading.Thread(target=worker, args=[inotify, lock])
            threads.append(t)
            t.start()
    finally:
        for i in range(num_of_threads):
            threads[i].join()

        # Stop watching the registered dir
        inotify.unwatch(mydir)

        # We no longer interested to monitor anything, lets tell the kernel
        inotify.close()

sys.exit(0)
