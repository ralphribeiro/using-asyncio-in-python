import argparse
import asyncio
import asyncpg
from asyncpg.pool import Pool

DSN = 'postgresql://{user}@{host}:{port}'
DSN_DB = DSN + '/{name}'
CREATE_DB = 'CREATE DATABASE {name}'
DROP_DB = 'DROP DATABASE {name}'


class Database:
    def __init__(self, name, owner=False, **kwargs):
        self.params = dict(
            user='postgres', host='localhost',
            # The Database class is just a fancy context manager for creating
            # and deleting a database from a PostgreSQL instance. The database
            # name is passed into the constructor.
            port='55432', name=name,
        )
        self.params.update(kwargs)
        self.pool: Pool = None
        self.owner = owner
        self.listeners = []

    async def connect(self) -> Pool:
        if self.owner:
            # Here, in the entering side, I’ll create the new database and
            # return a connection to that new database. server_command() is
            # another helper method defined a few lines down. I use it to run
            # the command for creating our new database.
            await self.server_command(CREATE_DB.format(**self.params))

        # I then make a connection to the newly created database. Note that
        # I’ve hardcoded several details about the connection: this is
        # intentional, as I wanted to keep the code samples small. You could
        # easily generalize this by making fields for the username, hostname,
        # and port.
        self.pool = await asyncpg.create_pool(DSN_DB.format(**self.params))
        return self.pool

    async def disconnect(self):
        """Destroy the database"""
        if self.pool:
            releases = [self.pool.release(conn) for conn in self.listeners]
            await asyncio.gather(*releases)
            # In the exiting side of the context manager, I close the
            # connection and...
            await self.pool.close()
        if self.owner:
            # ...destroy the database.
            await self.server_command(DROP_DB.format(**self.params))

    # (Note: The sequence of callouts in the code is intentionally different
    # from this list.) This is an asynchronous context manager. Instead of the
    # usual __enter__() and __exit__() methods, I use their __aenter__() and
    # __aexit__() counterparts.
    async def __aenter__(self) -> Pool:
        return await self.connect()

    async def __aexit__(self, *exc):
        await self.disconnect()

    # For completeness, this is our utility method for running commands against
    # the PostgreSQL server itself. It creates a connection for that purpose,
    # runs the given command, and exits.
    async def server_command(self, cmd):
        conn = await asyncpg.connect(DSN.format(**self.params))
        await conn.execute(cmd)
        await conn.close()

    # This function creates a long-lived socket connection to the database that
    # will listen for events. This mechanism will be featured in the upcoming
    # case study.
    async def add_listener(self, channel, callback):
        conn: asyncpg.Connection = await self.pool.acquire()
        await conn.add_listener(channel, callback)
        self.listeners.append(conn)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cmd', choices=['create', 'drop'])
    parser.add_argument('--name', type=str)
    args = parser.parse_args()
    d = Database(args.name, owner=True)
    if args.cmd == 'create':
        asyncio.run(d.connect())
    elif args.cmd == 'drop':
        asyncio.run(d.disconnect())
    else:
        parser.print_help()
