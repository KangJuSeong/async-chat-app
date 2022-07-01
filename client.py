import aiohttp
import asyncio


async with session.ws_connect('http://localhost:8080/ws') as ws:
    print(ws)
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close cmd':
                await ws.close()
                break
            else:
                await ws.send_str('hello' + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            break

