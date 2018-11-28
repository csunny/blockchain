#!/usr/bin/env python3

import asyncio
import sys

async def client(loop):
    reader, writer = await asyncio.open_connection("127.0.0.1", 9090, loop=loop)
    while True:
        data = await reader.read(100)
        message = data.decode()
        print(message)

        tin = sys.stdin.readline()
        writer.write(tin.encode())
        await writer.drain()

loop = asyncio.get_event_loop()
loop.run_until_complete(client(loop))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

loop.close()
