import asyncio
import websockets
import json

fn = "linus.jpg"
uri = f"ws://localhost:5000/bogodownload/{fn}"

client_dir = "client_files"

async def hello():
    ls = [None]
    async with websockets.connect(uri) as websocket:
        last = -1
        iters = 0
        while None in ls:
            resp = await websocket.recv()
            resp = json.loads(resp)
            size = resp["size"]

            if len(ls) != size:
                ls = [None] * size

            ls[resp["pos"]] = resp["byte"]

            now = sum(1 for i in ls if i != None)
            if now > last:
                last = now
                print(f"{now}/{len(ls)}")
            
            iters += 1
        

    with open(f"{client_dir}/{fn}", "wb+") as w:
        w.write(bytes(ls))
    
    print(f"Received {fn} ({size} bytes) in ({iters} byte transfers). (In)efficiency: {(iters/size) * 100}%")

asyncio.get_event_loop().run_until_complete(hello())
