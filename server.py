from aiohttp import web
import asyncio


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.sedn_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print("ws connection closed with exception %s" %ws.exception())

    print("websocket, connection closed")

    return ws

app = web.Application()
app.add_routes([web.get('/ws', websocket_handler)])

