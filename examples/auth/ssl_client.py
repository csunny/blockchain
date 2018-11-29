#!/usr/bin/env python3

import sys
import ssl
import asyncio

async def echo_tcp_client(loop):
    ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ssl_context.check_hostname = False
    ssl_context.load_verify_locations('auth.crt')
    reader, writer = await asyncio.open_connection("127.0.0.1", 9999, loop=loop, ssl=ssl_context)

    while True:
        message = sys.stdin.readline()
        print("发送数据 %r" % message)
        writer.write(message.encode())
        await writer.drain()
        data = await reader.read(100)

        print("接收数据 %r" % data.decode())



loop = asyncio.get_event_loop()
loop.run_until_complete(echo_tcp_client(loop))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
loop.close()
        
        
        