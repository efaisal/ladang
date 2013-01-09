Tutorial: ladang - inotify Made Easy
====================================

You are only 6 steps away to fully utilize ladang. In this tutorial we will
monitor a directory for all possible inotify events.

Step One
--------
Import the module. ::

    import ladang

Step Two
--------
Instantiate ``ladang.Ladang()`` object. ::

    inotify = ladang.Ladang() # This call is for blocking get_event()

or ::

    inotify = ladang.Ladang(ladang.NONBLOCK|ladang.CLOEXEC) # This call for non-blocking get_event()

Step Three
----------

Next we register a file or a directory which we are interested to monitor and
event which we wish the kernel to notify us. By default all events will be
reported. ::

    inotify.watch('/path/to/mydir', ladang.IN_ALL_EVENTS)

The bit mask ``ladang.IN_ALL_EVENTS`` indicates we are interested in all events.
There are many other masks available which can be bitwise ORed. See :ref:`eventmask-constant`
for other possible values.

Step Four
---------

If any of the events we are interested in occur, inotify will put it into an
event queue. All we have to do is fetch the occured events from the queue.
First create a file in */path/to/mydir* so that there is a filesystem event
happen. Execute from the shell: ::

    $ touch /path/to/mydir/myfile

Then we can pull the events from the queue by doing: ::

    events = inotify.get_event()

If there is no inotify event, ``inotify.get_event()`` returns an empty tuple.
Else we can do this to print out the events: ::

    for event in events:
        print("Watch description: %d" % evt['wd'])
        print("Mask: %d" % evt['mask'])
        print("Mask descr: %s => %s" % ladang.INOTIFY_MASKS[evt['mask']])
        print("Cookie: %d" % evt['cookie'])
        print("Name: %s" % evt['name'].strip("\0"))

A word of cautious, if you are employing a multithreaded strategy, it is
important to employ a proper locking. This is because internally, the watched
file descriptor will be shared across all thread.

Step Five
---------

When you are no longer interested to monitor any event, just do: ::

    inotify.unwatch('/path/to/dir')

Step Six
--------

And when you're done, simply call the ``inotify.close()`` method to close the
controlling inotify file descriptor. ::

    inotify.close(notify_fd)

