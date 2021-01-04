# For educational purposes only, don’t do this!

import asyncio


async def f():
    try:
        while True:
            await asyncio.sleep(0)
    except asyncio.CancelledError:
        print('Nope!')
        while True:
            # Instead of printing a message, what happens if after
            # cancellation, we just go rightback to awaiting another
            # awaitable?
            await asyncio.sleep(0)
    else:
        return 111


coro = f()
coro.send(None)
# Unsurprisingly, our outer coroutine continues to live, and it immediately
# suspends again inside the new coroutine
coro.throw(asyncio.CancelledError)
# expected: "Nope!"

# Everything proceeds normally, and our coroutine continues to suspend
# and resume as expected.
coro.send(None)
