import asyncio
import asyncpg
import datetime
# I’ve hidden some boilerplate away in a tiny util module to simplify things
# and keep the core message.
from util import Database


async def main():
    # The Database class gives us a context manager that will create a new
    # database for us —in this, case named test— and will destroy that database
    # when the contextmanager exits. This turns out to be very useful when
    # experimenting with ideas incode. Because no state is carried over between
    # experiments, you start from a clean database every time. Note that this
    # is an async with context manager; we’ll talk more about that later, but
    # for now, the focal area of this demo is what happens inside the demo()
    # coroutine.
    async with Database('test', owner=True) as conn:
        await demo(conn)


async def demo(conn: asyncpg.Connection):
    await conn.execute('''
        CREATE TABLE users(
        id serial PRIMARY KEY,
        name text,
        dob date
        )'''
                       )
    # The Database context manager has provided us with a Connection instance,
    # which is immediately used to create a new table, users.

    # I use fetchval() to insert a new record. While I could have used
    # execute() todo the insertion, the benefit of using fetchval() is that I
    # can obtain the id of the newly inserted record, which I store in the pk
    # identifier.
    # Note that I use parameters ($1 and $2) for passing data to the SQL query.
    # Never use string interpolation or concatenation to build queries, as this
    # is a security risk!
    pk = await conn.fetchval(
        'INSERT INTO users(name, dob) VALUES($1, $2) '
        'RETURNING id', 'Bob', datetime.date(1984, 3, 1)
    )

    # In the remainder of this demo, I’m going to be manipulating data in the
    # users table, so here I make a new utility coroutine function that fetches
    # a record in the table. This will be called several times.

    async def get_row():
        # When retrieving data, it is far more useful to use the fetch-based
        # methods, because these will return Record objects. asyncpg will
        # automatically cast data‐types to the most appropriate types for
        # Python.
        return await conn.fetchrow(
            'SELECT * FROM users WHERE name = $1',
            'Bob'
        )
    # I immediately use the get_row() helper to display the newly inserted
    # record.
    print('After INSERT:', await get_row())

    await conn.execute(
        'UPDATE users SET dob = $1 WHERE id=1',
        # I modify data by using the UPDATE command for SQL. It’s a tiny
        # modification: the year value in the date of birth is changed by one
        # year. As before, this is performed with the connection’s execute()
        # method. The remainder of the code demo follows the same structure as
        # seen so far, and a DELETE, followed by another print(), happens a few
        # lines down.
        datetime.date(1985, 3, 1)
    )
    print('After UPDATE:', await get_row())

    await conn.execute(
        'DELETE FROM users WHERE id=1'
    )
    print('After DELETE:', await get_row())

if __name__ == '__main__':
    asyncio.run(main())
