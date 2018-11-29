#!/usr/bin/env python3

import asyncio 
async def hello():
    print("Hello world!")


loop = asyncio.get_event_loop()
loop.run_until_complete(hello())
loop.close()