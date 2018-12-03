#!/usr/bin/env python3 

import asyncio
from rpcudp.protocol import RPCProtocol


class RPCServer(RPCProtocol):
    # Any methods starting with "rpc_" are avaliable to clients 
    def rpc_sayhi(self, sender, name):
        # This could return a Deferred as well. sender is (ip, port)
        return "Hello %s you live at %s:%i" % (name, sender[0], sender[1])

    
# start a server on UDP port 1234
loop = asyncio.get_event_loop()
listen = loop.create_datagram_endpoint(RPCServer, local_addr=('127.0.0.1', 1234))
transport, protocol = loop.run_until_complete(listen)
loop.run_forever()
