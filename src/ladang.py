from _ladang import *

__version__ = '0.9.0'
__doc__ = """
This module provides the a high level, more Pythonic interface to inotify as
compared to the low level _ladang module, a low level C extension.
"""

class LadangError(IOError): pass

class Ladang(object):
    """
A wrapper class to _ladang to provide a more Pythonic interface to inotify.
    """
    _i_fd = None   # Inotify event queue file descriptor
    _watchers = {} # List of watchers
    _wd_map = {}   # Watch descriptor map to pathname
    _nonblock = False

    def __init__(self, flags=0):
        """
Ladang([flag=0])

Initializes a new Ladang instance.

If *flag* is 0 by default, suitable for most operation. However, for
non-blocking the following flags can be bitwise ORed:

==================    ==========================================================
Constant              Meaning
==================    ==========================================================
.. data:: NONBLOCK    Set the O_NONBLOCK file status flag to the file descriptor
.. data:: CLOEXEC     Set the FD_CLOEXEC flag to the file descriptor
==================    ==========================================================

Returns a Ladang object.
"""
        if flags & NONBLOCK: self._nonblock = True
        try:
            self._i_fd = init1(flags)
        except IOError as e:
            raise LadangError(*e.args)

    def __del__(self):
        try:
            self.close()
        except:
            pass

    def get_fd(self):
        """
get_fd()

Get the inotify event queue file descriptor.

Returns a file descriptor associated with inotify event queue.
"""
        return self._i_fd

    def close(self):
        """
close()

Close the control file descriptor of Ladang object.
"""
        try:
            if self._watchers:
                for w in self._watchers:
                    try:
                        self.remove_watcher(w)
                    except:
                        pass
            close(self._i_fd)
        except IOError as e:
            raise LadangError(*e.args)

    def watch(self, pathname, mask=IN_ALL_EVENTS):
        """
watch(pathname[, mask=ladang.IN_ALL_EVENTS])

Register a file or directory to watch on event(s) defined by *mask*. (see :ref:`eventmask-constant`)
"""
        if not self._i_fd:
            raise LadangError('inotify event queue not initialized')
        try:
            wd = add_watch(self._i_fd, pathname, mask)
            self._watchers[pathname] = {'wd': wd, 'mask': mask}
            self._wd_map[wd] = pathname
        except IOError as e:
            raise LadangError(*e.args)

    def unwatch(self, pathname):
        """
Unregister watched file or directory.
"""
        if pathname not in self._watchers:
            raise LadangError(2, 'No such file or directory', pathname)
        try:
            rm_watch(self._i_fd, self._watchers[pathname]['wd'])
            del self._wd_map[self._watchers[pathname]['wd']], self._watchers[pathname]
        except IOError as e:
            raise LadangError(*e.args)

    def get_event(self):
        """
get_event()

Fetch events on watched file or directory..

Each event will be represented as Python dictionary, with the following keys:

======    ========================================
Key       Meaning
======    ========================================
wd        Watched file of directory
mask      Mask of events
cookie    Unique cookie associating related events
name      Optional null-terminated name
======    ========================================

Returns a tuple of events.
"""
        events = []
        try:
            _events = get_event(self._i_fd)
            if _events:
                for evt in _events:
                    evt['wd'] = self._wd_map[evt['wd']]
                    if evt['len'] > 0:
                        evt['name'] = evt['name'].strip('\0')
                    else:
                        evt['name'] = None
                    del evt['len']
                    events.append(evt)
        except IOError as e:
            raise LadangError(*e.args)
        return tuple(events)
