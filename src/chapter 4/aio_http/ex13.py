from aiohttp import web


async def hello(request):
    return web.Response(text='Wello world')


# An Application instance is created.
app = web.Application()
app.router.add_get('/', hello)
web.run_app(app, port=8080)