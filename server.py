from quart import Quart, websocket
import asyncio
import random
import json
import os

app = Quart(__name__)

interval = 0
server_dir = "server_files"

@app.websocket('/bogodownload/<fn>')
async def bogo(fn):
    filename = None
    for f in os.listdir(server_dir):
        if f == fn and os.path.isfile(f"{server_dir}/{f}"):
            filename = f
    if not filename:
        return
    
    with open(f"{server_dir}/{filename}", "rb") as o:
        to_send = list(o.read())
        bytelength = len(to_send)

    try:
        while True:
            bytepos = random.randint(0, bytelength-1)
            await websocket.send(
                json.dumps(
                    {
                        "size": bytelength,
                        "pos": bytepos,
                        "byte": to_send[bytepos]
                    }
                )
            )
            await asyncio.sleep(interval)
    finally:
        ...

app.run()