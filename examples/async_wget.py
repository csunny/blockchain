#!/usr/bin/env python3

import asyncio

async def wget(host):
    print("wget %s ...", host)
    connect = asyncio.open_connection(host, 80)
    reader, writer = await connect

    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
    writer.write(header.encode())
    await writer.drain()

    while True:
        line = await reader.readline()
        if line == b'\r\n':
            break
        print("%s header > %s" % (host, line.decode().rstrip()))
    
    writer.close()


loop = asyncio.get_event_loop()
tasks = [wget(host) for host in ["www.sina.com", "www.sohu.com", "www.163.com"]]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

    