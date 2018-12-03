#!/usr/bin/env python3

import asyncio


class EchoServerProtocol:
    def connection_made(self, transport):
        self.transport = transport
    
    def datagram_received(self, data, addr):
        message = data.decode()
        print("Received %r from %s" % (message, addr))
        print("Send %r to %s" % (message, addr)) 
        self.transport.sendto(data, addr)
    

async def main():
    print("Starting UDP server")
    # Get a reference to the event loop as we plan to use low-level apis
    loop = asyncio.get_running_loop()

    # Once protocol instance will be created to server all client requests 
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: EchoServerProtocol(),
        local_addr = ('127.0.0.1', 9999)
    )

    try:
        await asyncio.sleep(3600)
    finally:
        transport.close()
    
asyncio.run(main())