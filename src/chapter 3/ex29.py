# Destroyer of pending tasks
import asyncio


async def f(delay):
    await asyncio.sleep(delay)


loop = asyncio.get_event_loop()
t1 = loop.create_task(f(1))
t2 = loop.create_task(f(2))

# Run only until task 1 is complete.
loop.run_until_complete(t1)
loop.close()
