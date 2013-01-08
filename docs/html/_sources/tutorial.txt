Tutorial: ladang - inotify Made Easy
====================================

You are only 6 steps away to fully utilize ladang:

Step One
--------
Import the module. ::

    import ladang

Step Two
--------
Get a file descriptor associated with a new inotify event queue. ::

    notify_fd = ladang.init() # This call is blocking

or ::

    notify_fd = ladang.init1(ladang.NONBLOCK|ladang.CLOEXEC) # This call is non-blocking

Step Three
----------

Next we add or create a new watch for file or directory we are interested to
monitor. For example, if we are interested to monitor some events for
*/path/to/mydir* for all events, we can tell the inotify event queue to tell us
when the event occur by doing: ::

    watch_fd = ladang.add_watch(notify_fd, '/path/to/mydir', ladang.IN_ALL_EVENTS)

The bit mask ``ladang.IN_ALL_EVENTS`` indicates we are interested in all events.
There are many other masks available which can be bitwise ORed. See :ref:`addwatch-constant`
for other possible values.

Step Four
---------

If any of the events we are interested in occur, inotify will put it into an
event queue. All we have to do is fetch the occured events from the queue.
First create a file in */path/to/mydir* so that there is a filesystem event
happen. Execute from the shell: ::

    $ touch /path/to/mydir/myfile

Then we can pull the events from the queue by doing: ::

    events = ladang.get_event(notify_fd)
    for event in events:
        print("Watch description: %d" % evt['wd'])
        print("Mask: %d" % evt['mask'])
        print("Mask descr: %s => %s" % ladang.INOTIFY_MASKS[evt['mask']])
        print("Cookie: %d" % evt['cookie'])
        print("Length: %d" % evt['len'])
        print("Name: %s" % evt['name'].strip("\0"))

Calling ``ladang.get_event()`` will also empty the event queue. Therefore, if
you want to get more events from the queue, simply call it repeatedly.

If in the second step you use ``ladang.init()``, the call ``ladang.get_event()``
will block. If you use ``ladang.init1()``, ``ladang.get_event()`` will return
immediately, either list of events or an empty list. If you are employing a
multithreaded strategy, it's worth mentioning that *notify_fd* is typically a
shared resource, so proper locking is usually required.

Step Five
---------

When you are no longer interested watching the event, just do: ::

    ladang.rm_watch(watch_fd)

Step Six
--------

And when you're done, simply close the inotify event queue file descriptor. ::

    ladang.close(notify_fd)

