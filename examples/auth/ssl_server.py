#!/usr/bin/env python3

import asyncio
import ssl

async def handle_echo(reader, writer):
    while True:

        data = await reader.read(100)
        message = data.decode()

        addr = writer.get_extra_info('peername')
        print("> 接收到数据%s From %r" %(message, addr))

        print("> 发送数据 %r" % message)
        writer.write(data)
        await writer.drain()


ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.check_hostname = False
ssl_context.load_cert_chain('auth.crt', 'auth.key')


loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', 9999, ssl=ssl_context)
server = loop.run_until_complete(coro)

print("Server on", server.sockets[0].getsockname())

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()