from aiohttp import web
import asyncio


async def hello(request):
    return web.Response(text='Hello, World')
    
app = web.Application()
app.add_routes([web.get('/', hello)])
web.run_app(app)

