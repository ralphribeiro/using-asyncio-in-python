### just a  small  subset  of  the  whole asyncio API

- Starting the asyncio event loop
- Calling async/await functions
- Creating a task to be run on the loop
- Waiting for multiple tasks to complete
- Closing the loop after all concurrent tasks have completed

----------

### Features of asyncio arranged in a hierarchy; for end-user developers, the mostimportant tiers are highlighted in bold

Level | Concept | Implementation

--- | --- | ---

**tier 9** | **Network: streams** | StreamReader, StreamWriter, asyncio.open_connection(), asyncio.start_server()
tier 8 | Network: TCP & UDP | Protocol
tier 7 | Network: transports | BaseTransport
**tier 6** | **Tools** | asyncio.Queue
**tier 5** | Subprocess & Threads | run_in_executor(), asyncio.subprocess
tier 4 | Tasks | asyncio.Task, asyncio.create_task()
tier 3 | Futures | asyncio.Future
**tier 2** | **Event loop** | asyncio.run(), BaseEventLoop
**tier 1 (Base)** | **Coroutines** | async def, async with, async for, await
