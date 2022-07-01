from aiohttp import web
import aiohttp
import asyncio
import random
from collections import defaultdict


async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    room = 'test_room'
    user = await ws.receive_str()
    print(f'[{user}] connection success')
    await ws.send_str(f'[{user}] Welcome chat app.')
    
    if request.app['websockets'][room].get(user):
        await ws.close(message=b'Aready User')
        return ws
    else:
        request.app['websockets'][room][user] = ws
        for ws in request.app['websockets'][room].values():
            await broadcast(request.app, message={'user': 'SYSTEM', 'message': f'[{user}] enter chat room'})

    async for msg in ws:
        if msg.type == web.WSMsgType.text:
            message = msg.json() 
            await broadcast(request.app, message)        
    
    print(f'[{user}] connection closed')

    return ws
    

async def broadcast(app, message):
    for user, ws in app['websockets']['test_room'].items():
        await ws.send_json(message)

app = web.Application()
app.add_routes([web.get('/ws', websocket_handler)])
app['websockets'] = defaultdict(dict)
web.run_app(app)

