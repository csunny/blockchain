#!/usr/bin/env python3
# -*- coding:utf-8
import asyncio
from common.settings import Blockchain
from p2p.peer import candidate, pick_winner, candidate_blocks, announcements, handle_conn


def main():
    loop = asyncio.get_event_loop()
    core = asyncio.start_server(handle_conn, '127.0.0.1', 9090, loop=loop)

    server = loop.run_until_complete(core)

    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


    
if __name__ == '__main__':
    main()






