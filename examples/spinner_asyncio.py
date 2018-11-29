#!/usr/bin/env python3 

import asyncio
import itertools
import sys

async def spin(msg):
    write, flush = sys.stdout.write, sys.stdout.flush

    for char in itertools.cycle("|/-\\"):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            await asyncio.sleep(1)
        except asyncio.CancelledError:
            break
        
    write(' ' * len(status) + '\x08' * len(status))

async def slow_function():
    await asyncio.sleep(3)
    return 42

async def supervisor():
    spinner = asyncio.ensure_future(spin("thinking"))
    print("spinner object:", spinner)
    result = await slow_function()
    spinner.cancel()
    return result

def main():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(supervisor())
    loop.close()
    print("Answer", result)

if __name__ == '__main__':
    main()