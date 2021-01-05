# Creating a task inside a cancellation handler
import asyncio
from asyncio import StreamReader, StreamWriter


# Pretend that this coroutine actually contacts an external server to
# submit event notifications.
async def send_event(msg: str):
    await asyncio.sleep(1)


async def echo(reader: StreamReader, writer: StreamWriter):
    print('New Connection.')
    try:
        while data := await reader.readline():
            writer.write(data.upper())
            await writer.drain()
        print('Leaving connection.')
    except asyncio.CancelledError:
        msg = 'Connection dropped'
        print(msg)
        # Because the event notifier involves network access, it is common for
        # such calls to be made in a separate async task; that’s why we’re
        # using the create_task() function here.
        asyncio.create_task(send_event(msg))


async def main(host='127.0.0.1', port=8888):
    server = await asyncio.start_server(echo, host, port)
    async with server:
        await server.serve_forever()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Bye!')

# To understand why this is happening, we must go back to the sequence of
# cleanupvents that asyncio.run() does during the shutdown phase; in
# particular, the important part is that when we press Ctrl-C, all the
# currently active tasks are collected and cancelled. At this point, only
# those tasks are then awaited, and asyncio.run() returns immediately after
# that. The bug in our modified code is that we created a new task inside the
# cancellation handler of our existing “echo” task. This new task was created
# only after asyncio.run() had collected and cancelled all the tasks
# in the process.
