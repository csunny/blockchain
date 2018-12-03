#!/usr/bin/env python3

import asyncio 
from rpcudp.protocol import RPCProtocol

async def sayhi(protocol, address):
    result = await protocol.sayhi(address, "Magic Hi")
    print(result[1] if result[0] else "No response received.")


# Start local UDP server to be able to handle responses
loop = asyncio.get_event_loop()
listen = loop.create_datagram_endpoint(RPCProtocol, local_addr=("127.0.0.1", 4567))
transport, protocol = loop.run_until_complete(listen)

# Call remote UDP server to say hi
func = sayhi(protocol, ('127.0.0.1', 1234))
loop.run_until_complete(func)
loop.run_forever()