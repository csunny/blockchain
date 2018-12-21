#!/usr/bin/env python3

import asyncio

async def echo_tcp_client(message, loop):
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888, loop=loop)
    
    print("发送数据: %r" % message)
    writer.write(message.encode())

    data = await reader.read(100)
    print("接收数据: %r" % data.decode())

    print("关闭socket连接")
    writer.close()

message = "Hello World!"
loop = asyncio.get_event_loop()
loop.run_until_complete(echo_tcp_client(message, loop))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
    
loop.close()
