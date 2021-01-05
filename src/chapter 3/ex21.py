# The blocking way
from contextlib import contextmanager

# The @contextmanager decorator transforms a generator function into a
# contextmanager.
@contextmanager
def web_page(url):
    # This function call (which I made up for this example) looks suspiciously
    # like the sort of thing that will want to use a network interface, which
    # is many orders of magnitude slower than “normal” CPU-bound code. This
    # context manager must be used in a dedicated thread; otherwise, the whole
    # program will be paused while waiting for data.
    data = download_webpage(url)
    yield data

    # Imagine that we update some statistics every time we process data from a
    # URL,such as the number of times the URL has been downloaded. From a
    # concurrency perspective, we would need to know whether this function
    # involves I/O internally, such as writing to a database over a network.
    # If so, update_stats() is also a blocking call.
    update_status(url)


# Our context manager is being used. Note specifically how the network call
# (todownload_webpage()) is hidden inside the construction of the context
# manager.
with web_page('dgg.gg') as data:
    # This function call, process(), might also be blocking. We’d have to look
    # at whatthe function does, because the distinction between what is
    # blocking or nonblocking is not clear-cut. It might be:
    # ** Innocuous and nonblocking (fast and CPU-bound)
    # ** Mildly blocking (fast and I/O-bound, perhaps something like fast disk
    #    accessinstead of network I/O)
    # ** Blocking (slow and I/O-bound)
    # ** Diabolical (slow and CPU-bound)
    # 
    # For the sake of simplicity in this example, let’s presume that the call
    # to process() is a fast, CPU-bound operation and therefore nonblocking.
    process(data)
