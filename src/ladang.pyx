from libc.errno cimport *
from libc.string cimport strerror
from libc.stdint cimport *
cimport posix.unistd
from cinotify cimport *

__version__ = '0.8.0'
__doc__ = """
.. moduleauthor: E A Faisal <eafaisal at gmail dot com>

Yet another inotify binding. Minimum requirement is a Linux kernel 2.6.26.

This module creates a very thin layer to the inotify API. It also added 2 new
function calls:

- get_event()
- close()

in addition to the direct binding to inotify API.

get_event() provides a C-layer read()-ing and translating inotify events into
Python dictionary. close() provides a C-layer close() function call to inotify
instance file descriptor.

On top of that, this module attempts to throw Python exception on error and
exposes a Python dictionary INOTIFY_MASKS to facilitate translating the event
mask in the event dictionary.
"""

# Supported events suitable for MASK parameter of INOTIFY_ADD_WATCH.
IN_ACCESS = 0x00000001 # File was accessed.
IN_MODIFY = 0x00000002 # File was modified.
IN_ATTRIB = 0x00000004 # Metadata changed.
IN_CLOSE_WRITE = 0x00000008 # Writtable file was closed.
IN_CLOSE_NOWRITE = 0x00000010 # Unwrittable file closed.
IN_CLOSE = IN_CLOSE_WRITE | IN_CLOSE_NOWRITE # Close.
IN_OPEN = 0x00000020 # File was opened.
IN_MOVED_FROM = 0x00000040 # File was moved from X.
IN_MOVED_TO = 0x00000080 # File was moved to Y.
IN_MOVE = IN_MOVED_FROM | IN_MOVED_TO # Moves.
IN_CREATE = 0x00000100 # Subfile was created.
IN_DELETE = 0x00000200 # Subfile was deleted.
IN_DELETE_SELF = 0x00000400 # Self was deleted.
IN_MOVE_SELF = 0x00000800 # Self was moved.

# Events sent by the kernel.
IN_UNMOUNT = 0x00002000 # Backing fs was unmounted.
IN_Q_OVERFLOW = 0x00004000 # Event queued overflowed.
IN_IGNORED = 0x00008000 # File was ignored.

# Special flags.
IN_ONLYDIR = 0x01000000 # Only watch the path if it is a directory.
IN_DONT_FOLLOW = 0x02000000 # Do not follow a sym link.
IN_EXCL_UNLINK = 0x04000000 # Exclude events on unlinked objects.
IN_MASK_ADD = 0x20000000 # Add to the mask of an already existing watch.
IN_ISDIR = 0x40000000 # Event occurred against dir.
IN_ONESHOT = 0x80000000 # Only send event once.

# All events which a program can wait on.
IN_ALL_EVENTS = IN_ACCESS | IN_MODIFY | IN_ATTRIB | IN_CLOSE_WRITE | \
                IN_CLOSE_NOWRITE | IN_OPEN | IN_MOVED_FROM | IN_MOVED_TO | \
                IN_CREATE | IN_DELETE | IN_DELETE_SELF | IN_MOVE_SELF

# Constant description
INOTIFY_MASKS = {IN_ACCESS: ('IN_ACCESS', 'File was accessed.'),
                 IN_MODIFY: ('IN_MODIFY', 'File was modified.'),
                 IN_ATTRIB: ('IN_ATTRIB', 'Metadata changed.'),
                 IN_CLOSE_WRITE: ('IN_CLOSE_WRITE', 'Writtable file was closed.'),
                 IN_CLOSE_NOWRITE: ('IN_CLOSE_NOWRITE', 'Unwrittable file closed.'),
                 IN_CLOSE: ('IN_CLOSE', 'Close.'),
                 IN_OPEN: ('IN_OPEN', 'File was opened.'),
                 IN_MOVED_FROM: ('IN_MOVED_FROM', 'File was moved from X.'),
                 IN_MOVED_TO: ('IN_MOVED_TO', 'File was moved to Y.'),
                 IN_MOVE: ('IN_MOVE', 'Moves.'),
                 IN_CREATE: ('IN_CREATE', 'Subfile was created.'),
                 IN_DELETE: ('IN_DELETE', 'Subfile was deleted.'),
                 IN_DELETE_SELF: ('IN_DELETE_SELF', 'Self was deleted.'),
                 IN_MOVE_SELF: ('IN_MOVE_SELF', 'Self was moved.'),
                 IN_UNMOUNT: ('IN_UNMOUNT', 'Backing fs was unmounted.'),
                 IN_Q_OVERFLOW: ('IN_Q_OVERFLOW', 'Event queued overflowed.'),
                 IN_IGNORED: ('IN_IGNORED', 'File was ignored.'),
                 IN_ONLYDIR: ('IN_ONLYDIR', 'Only watch the path if it is a directory.'),
                 IN_DONT_FOLLOW: ('IN_DONT_FOLLOW', 'Do not follow a sym link.'),
                 IN_EXCL_UNLINK: ('IN_EXCL_UNLINK', 'Exclude events on unlinked objects.'),
                 IN_MASK_ADD: ('IN_MASK_ADD', 'Add to the mask of an already existing watch.'),
                 IN_ISDIR: ('IN_ISDIR', 'Event occurred against dir.'),
                 IN_ONESHOT: ('IN_ONESHOT', 'Only send event once.')}

CLOEXEC = IN_CLOEXEC
NONBLOCK = IN_NONBLOCK

_BLOCKFD_LIST = []

cpdef int init() except -1:
    """
init()

Initializes a new inotify instance.

Returns a file descriptor associated with a new inotify event queue.
"""
    cdef int notification_fd
    notification_fd = inotify_init()
    if notification_fd == -1:
        raise OSError(errno, strerror(errno))
    _BLOCKFD_LIST.append(notification_fd)
    return notification_fd

cpdef int init1(int flags) except - 1:
    """
init1(flags)

Initializes a new inotify instance.

If *flags* is 0, init1 is the same as init(). The flag can be bitwise ORed using
the following values:

==================    ==========================================================
Constant              Meaning
==================    ==========================================================
.. data:: NONBLOCK    Set the O_NONBLOCK file status flag to the file descriptor
.. data:: CLOEXEC     Set the FD_CLOEXEC flag to the file descriptor
==================    ==========================================================

Returns a file descriptor associated with a new inotify event queue.
"""
    cdef int notification_fd
    notification_fd = inotify_init1(flags)
    if notification_fd == -1:
        raise OSError(errno, strerror(errno))
    if not flags & IN_NONBLOCK: _BLOCKFD_LIST.append(notification_fd)
    return notification_fd

cpdef int add_watch(int fd, char* pathname, int mask) except -1:
    """
add_watch(fd, pathname, mask)

Adds a watch to an initialized inotify instance associated with file
descriptor fd.

This functions adds a new watch, or modifies an existing watch, for the file
whose location is specified in pathname. The event to be monitored is specified
by setting the bits in mask.

*fd* is the inotify file descriptor as returned by *init()* or *init1()*.
*pathname* is either a file or directory to watch. *mask* is the inotify event
flags (see :ref:`addwatch-constant`).

Returns a watch descriptor on success.
    """
    cdef int watch_fd
    watch_fd = inotify_add_watch(fd, pathname, mask)
    if watch_fd == -1:
        raise OSError(errno, strerror(errno))
    return watch_fd

cpdef int rm_watch(int fd, int wd) except -1:
    """
rm_watch(fd, wd)

Remove an existing watch from inotify instance.

This function removes the watch associated with the watch descriptor *wd* from 
inotify instance associated with the file descriptor *fd*.

Removing a watch will cause IN_IGNORED to be generated for this watch descriptor.

Returns 0 on success.
"""
    cdef int ret_val
    ret_val = inotify_rm_watch(fd, wd)
    if ret_val == -1:
        raise OSError(errno, strerror(errno))
    return ret_val

cpdef int close(int fd) except -1:
    """
close(fd)

Close inotify instance associated with file descriptor *fd*.

Returns 0 on success.
"""
    ret_val = posix.unistd.close(fd)
    if fd in _BLOCKFD_LIST:
        del _BLOCKFD_LIST[_BLOCKFD_LIST.index(fd)]
    if ret_val == -1:
        raise OSError(errno, strerror(errno))
    return ret_val

cpdef object get_event(int fd) with gil:
    """
get_event(fd)

Fetch event occuring from inotify instance associated with file descriptor *fd*.

Each event will be represented as Python dictionary, with the following keys:

======    ========================================
Key       Meaning
======    ========================================
wd        Watch descriptor
mask      Mask of events
cookie    Unique cookie associating related events
len       Size of name field
name      Optional null-terminated name
======    ========================================

Returns a list of events.
"""
    cdef int length = 0
    cdef int i = 0
    cdef char cbuffer[EVENT_BUFFER_LENGTH]
    cdef inotify_event* event
    cdef inotify_event evt

    # List of events
    events = []

    while True:
        length = posix.unistd.read(fd, cbuffer, EVENT_BUFFER_LENGTH)
        if length == -1:
            if errno == EAGAIN: break
            raise OSError(errno, strerror(errno))

        while i < length:
            # event is a pointer and referenced to cbuffer address
            event = <inotify_event* ?> &cbuffer[i]
            # instead of doing *event, in cython needs to do event[0] instead for dereferencing
            # evt is intofy_event struct
            evt = event[0]
            if evt.len:
                ret_val = {'wd': evt.wd, 'mask': evt.mask,
                           'cookie': evt.cookie, 'len': evt.len,
                           'name': cbuffer[i+EVENT_SIZE:i+EVENT_SIZE+evt.len]}
                #events.append(<object ?> evt)
                events.append(ret_val)
            i += EVENT_SIZE + evt.len
        if fd in _BLOCKFD_LIST: break

    return events
