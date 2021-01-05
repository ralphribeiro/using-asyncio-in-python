# Async context manager


class Connection:
    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port

    # Instead of the __enter__() special method for synchronous context
    # managers, the new __aenter__() special method is used. This special
    # method must be an async def method.
    async def __aenter__(self):
        self.conn = await get_conn(self.host, self.port)
        return conn

    # Likewise, instead of __exit__(), use __aexit__(). The parameters are
    # identical to those for __exit__() and are populated if an exception was
    # raised in the body of the context manager.
    async def __aexit__(self, exc_type, exc, tb):
        self.conn.close()

async with Connection('localhost', 9001) as conn:
    <do stuff with conn>
