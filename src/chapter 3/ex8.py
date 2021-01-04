import asyncio


async def f():
    await asyncio.sleep(1.0)
    return 123


# As before, a new coroutine is created from the coroutine function f()
coro = f()
coro.send(None)
# Instead of doing another send(), we call throw() and provide an exception
# classand a value. This raises an exception inside our coroutine, at the
# await point.
coro.throw(Exception, 'blah')
