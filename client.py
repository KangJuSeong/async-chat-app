from aioconsole import ainput
import aiohttp   
import asyncio


async def send_message(ws, user):
    while True:
        message = await ainput()
        await ws.send_json({'user': user, 'message': message})

async def receive_message(ws):
    async for msg in ws:
        if msg.type == aiphttp.web.WSMsgType.text: 
            msg_json = msg.json()
            print(f">>> [{msg_json['user']}] : {msg_json['message']})")
    
async def handler(user):
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('http://localhost:8080/ws') as ws:
            await ws.send_str(user)
            print(await ws.receive_str())
         
            send_message_task = asyncio.create_task(send_message(ws, user))
            receive_message_task = asyncio.create_task(receive_message(ws))
            done, pending = await asyncio.wait(
                    [receive_message_task, send_message_task], return_when=asyncio.FIRST_COMPLETED,
            )

user = input('Input name : ')
asyncio.run(handler(user))
