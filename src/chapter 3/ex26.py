# Easier with an async generator
import asyncio
from aioredis import create_redis


# The main() function is identical to the version in ex25.
async def main():
    redis = await create_redis(('localhost', 6379))
    keys = ['Americas', 'Africa', 'Europe', 'Asia', 'Oceania']

    # Well, almost identical: I changed the name from
    # CamelCase to snake_case.
    async for value in one_at_a_time(redis, keys):
        await in do_something_with(value)

# Our function is now declared with async def, making it a coroutine function,
# and since this function also contains the yield keyword, we refer to it as
# an asynchro‐nous generator function.
async def one_at_a_time(redis, keys):
    for k in keys:
        # We don’t have to do the convoluted things necessary in the previous
        # example with self.ikeys: here, we just loop over the keys directly
        # and obtain the value...
        value = await redis.get(k)
        # ...and then yield it to the caller, just like a normal generator.
        yield value


asyncio.run(main())
