#include <sys/inotify.h>
#include <limits.h>

// event size
#define EVENT_SIZE (sizeof (struct inotify_event))
 
// define large enough buffer
#define EVENT_BUFFER_LENGTH (1024 * EVENT_SIZE + NAME_MAX + 1)
