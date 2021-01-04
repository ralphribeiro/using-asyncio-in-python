# Always getting the same event loop
import asyncio

loop = asyncio.get_event_loop()
loop2 = asyncio.get_event_loop()

# Both identifiers, loop and loop2, refer to the same instance.
assert loop is loop2
