ladang - High Level API
=======================

.. automodule:: ladang
   :members:

.. _eventmask-constant:

Inotify event mask constants
------------------------------
.. data:: IN_ACCESS

    File was accessed.

.. data:: IN_MODIFY

    File was modified.

.. data:: IN_ATTRIB

    Metadata changed.

.. data:: IN_CLOSE_WRITE

    Writtable file was closed.

.. data:: IN_CLOSE_NOWRITE

    Unwrittable file closed.

.. data:: IN_CLOSE

    Equivalent to ladang.IN_CLOSE_WRITE | ladang.IN_CLOSE_NOWRITE

.. data:: IN_OPEN

    File was opened.

.. data:: IN_MOVED_FROM

    File was moved from X.

.. data:: IN_MOVED_TO

    File was moved to Y.

.. data:: IN_MOVE

    Equivalent to ladang.IN_MOVED_FROM | ladang.IN_MOVED_TO

.. data:: IN_CREATE

    Subfile was created.

.. data:: IN_DELETE

    Subfile was deleted.

.. data:: IN_DELETE_SELF

    Self was deleted.

.. data:: IN_MOVE_SELF

    Self was moved.

.. data:: IN_ONLYDIR

    Only watch the path if it is a directory.

.. data:: IN_DONT_FOLLOW

    Do not follow a sym link.

.. data:: IN_EXCL_UNLINK

    Exclude events on unlinked objects.

.. data:: IN_MASK_ADD

    Add to the mask of an already existing watch.

.. data:: IN_ISDIR

    Event occurred against dir.

.. data:: IN_ONESHOT

    Only send event once.

.. data:: IN_ALL_EVENTS

    All events which can be waited on.

    Equivalent to: 

    ladang.IN_ACCESS | ladang.IN_MODIFY | ladang.IN_ATTRIB | ladang.IN_CLOSE_WRITE | \
    ladang.IN_CLOSE_NOWRITE | ladang.IN_OPEN | ladang.IN_MOVED_FROM | ladang.IN_MOVED_TO | \
    ladang.IN_CREATE | ladang.IN_DELETE | ladang.IN_DELETE_SELF | ladang.IN_MOVE_SELF

