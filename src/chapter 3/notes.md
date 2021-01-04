### just a  small  subset  of  the  whole asyncio API

- Starting the asyncio event loop
- Calling async/await functions
- Creating a task to be run on the loop
- Waiting for multiple tasks to complete
- Closing the loop after all concurrent tasks have completed

----------

### Features of asyncio arranged in a hierarchy; for end-user developers, the mostimportant tiers are highlighted in bold

Level | Concept | Implementation
----- | ------- | --------------
**tier 9** | **Network: streams** | StreamReader, StreamWriter, asyncio.open_connection(), asyncio.start_server()
tier 8 | Network: TCP & UDP | Protocol
tier 7 | Network: transports | BaseTransport
**tier 6** | **Tools** | asyncio.Queue
**tier 5** | **Subprocess & Threads** | run_in_executor(), asyncio.subprocess
tier 4 | Tasks | asyncio.Task, asyncio.create_task()
tier 3 | Futures | asyncio.Future
**tier 2** | **Event loop** | asyncio.run(), BaseEventLoop
**tier 1 (Base)** | **Coroutines** | async def, async with, async for, await

----------

- Tier 1: Understanding how to write async def functions and use await to call and exe‐cute other coroutines is essential.
- Tier 2: Understanding how to start up, shut down, and interact with the event loop is essential.
- Tier 5: Executors are necessary to use blocking code in your async application, and the reality is that most third-party libraries are not yet asyncio-compatible. A good example of this is the SQLAlchemy database ORM library, for which no feature-comparable alternative is available right now for asyncio.
- Tier 6: If you need to feed data to one or more long-running coroutines, the best way todo that is with asyncio.Queue. This is exactly the same strategy as using queue.Queue for distributing data between threads. The Asyncio version of Queue uses the same API as the standard library queue module, but uses coroutines instead of the blocking methods like get().
- Tier 9: The streams API gives you the simplest way to handle socket communication over a network, and it is here that you should begin prototyping ideas for network applications. You may find that more fine-grained control is needed, and then you could switch to the protocols API, but in most projects it’s usually best to keep things simple until you know exactly what problem you’re trying to solve.

----------

The [pysheeet](https://www.pythonsheets.com/notes/python-asyncio.html) site provides an in-depth summary (or “cheat sheet”)of large chunks of the asyncio API; each concept is presented with a short code snippet. The presentation is dense, so I wouldn’t rec‐ommend it for beginners, but if you have experience with Pythonand you’re the kind of person who “gets it” only when new pro‐gramming info is presented in code, this is sure to be a usefulresource.

----------

*await* keyword: This new keyword await always takes a parameter and will accept only a thing called an awaitable, which is defined as one of these (exclusively!):
- A coroutine
- Any object implementing the __await__() special method. That special methodmust return an iterator.

event loop: You can get by without ever needing to work with the event loop directly: your asyncio code can be written entirely using await calls, initiated by an asyncio.run(coro)call. However, at times some degree of interaction with the event loop itself might benecessary, and here we’ll discuss how to obtain it. There are two ways:
- *Recommended* - asyncio.get_running_loop(), callable from inside the context of a coroutine
- *Discouraged* - asyncio.get_event_loop(), callable from anywhere

Tasks and Futures: 
- a Future represents a future completion stateof some activity and is managed by the loop. A Task is exactly the same, but the specific “activity” is a coroutine, probably one of yours that you created with an async def function plus create_task(). The Future class represents a state of something that is interacting with a loop. That description is too fuzzy to be useful, so you can instead think of a Future instance as a toggle for completion status. When a Future instance is created, the toggle is set to “not  yet  completed,”  but  at  some  later  time  it  will  be  “completed.”  In  fact,  a  Future instance has a method called done() that allows you to check the status, as shown in Example 3-15.
- Task  instances  are wrappers for coroutine objects, and their result values can be set only internally as theresult of the underlying coroutine function.