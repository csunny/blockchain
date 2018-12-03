#!/usr/bin/env python3

import asyncio

class EchoClientProtocol:
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop
        self.transport = None
        self.on_con_lost = loop.create_future()

    def connection_made(self, transport):
        self.transport = transport
        print("Send:", self.message)
        self.transport.sendto(self.message.encode())

    def datagram_received(self, data, addr):
        print("Received:", data.decode())

        print("Close the socket")
        self.transport.close()
    
    def error_received(self, exc):
        print("Connection closed")
        self.on_con_lost.set_result(True)

    def connection_lost(self, exc):
        print("Connection closed")
        self.on_con_lost.set_result(True)
    

async def main():
    # Get a reference to the event loop as we plan to use low-level APIs

    loop = asyncio.get_event_loop()
    message = "Hello world"

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: EchoClientProtocol(message, loop),
        remote_addr = ("127.0.0.1", 9999)
    )

    try:
        await protocol.on_con_lost
    finally:
        transport.close()


asyncio.run(main())
