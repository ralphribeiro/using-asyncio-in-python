# Async list, dict, and set comprehensions
import asyncio

async def doubler(n):
    for i in range(n):
        # is a very simple async generator: given an upper value, it’ll iterate
        # over a simple range, yielding a tuple of the value and its double.
        yield i, i * 2
        # Sleep a little, just to emphasize that this is really
        # an async function.
        await asyncio.sleep(0.1)

async def main():
    # An async list comprehension: note how async for is used instead of the
    # usual for. This difference is the same as that shown in the examples in
    # “Async Iterators: async for” on page 50
    result = [x async for x in doubler(3)]
    print(result)

    # An async dict comprehension; all the usual tricks work, such as unpacking
    # the tuple into x and y so that they can feed the dict comprehension syntax.
    result = {x: y async for x, y in doubler(3)}
    print(result)

    # The async set comprehension works exactly as you would expect.
    result = {x async for x in doubler(3)}
    print(result)
    

asyncio.run(main())