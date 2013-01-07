from libc.stdint cimport *

cdef extern from "sys/inotify.h":
    struct inotify_event:
      int wd # Watch descriptor.
      uint32_t mask # Watch mask.
      uint32_t cookie # Cookie to synchronize two events.
      uint32_t len # Length (including NULs) of name.
      char* name # Name.

    # inotify_init1 flags
    enum: IN_NONBLOCK
    enum: IN_CLOEXEC

    # Create and initialize inotify instance.
    extern int inotify_init ()
    extern int inotify_init1 (int __flags)

    # Add watch of object NAME to inotify instance FD.  Notify about
    # events specified by MASK.
    extern int inotify_add_watch (int __fd, char *__name, unsigned int __mask)

    # Remove the watch specified by WD from the inotify instance FD.
    extern int inotify_rm_watch (int __fd, int __wd)

cdef extern from "cutil.h":
    enum: EVENT_SIZE
    enum: EVENT_BUFFER_LENGTH
