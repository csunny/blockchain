#!/usr/bin/env python

import asyncio
from hashlib import sha256
from random import choice
import json
from datetime import datetime
from blockchain.block import generate_block, is_block_valid, caculate_hash
from common.settings import validators, Blockchain, tempblocks

candidate_blocks = asyncio.Queue()
announcements = asyncio.Queue()

async def handle_conn(reader, writer):
    client_host, client_port = writer.get_extra_info('peername')
    addr = "".join([client_host, ":", str(client_port)])
    print("Got connection from ", addr)

    # 提示客户端输入balance数量 
    writer.write(b"Enter token balance:")
    await writer.drain()
    
    balance_enc = await reader.read(100)
    try:
        balance = int(balance_enc.decode())
    except Exception as e:
        print(e)


    address = sha256(addr.encode()).hexdigest()
    validators[address] = balance
    print(validators)

    # asyncio.ensure_future(run())
    await run()

    while True:
        writer.write(b"Enter a new BPM:")

        await writer.drain()
        bpm_code = await reader.read(100)
        print("----", bpm_code)
        try:
            bpm = int(bpm_code.decode())
        except Exception as e:
            print(e)
            del validators[address]
            break

        last_block = Blockchain[-1]
        new_block = generate_block(last_block, bpm, address)
        if is_block_valid(new_block, last_block):
            print("new block is valid!")
            await candidate_blocks.put(new_block)
        
        writer.write(b"Enter a new BPM:\n")
        try:
            winner = await announcements.get()
            writer.write(winner.encode())
            writer.write(b'\n')
            await writer.drain()
        except asyncio.QueueEmpty:
            pass
        except IOError:
            pass

        try:
            bc = json.dumps(Blockchain)
            writer.write(bc.encode())
            await writer.drain()
        except IOError:
            pass

async def pick_winner(announcements):
    """
    选择记账人
    """
    while True:
        await asyncio.sleep(1)
        lottery_pool = []  #

        temp = tempblocks
        
        if temp:
            for block in temp:
                if block["Validator"] not in lottery_pool:
                    set_validator = validators
                    k = set_validator.get(block["Validator"])
                    # 根据持有的token数量构建票池, 持有的token数量与出现次数成正比
                    if k:
                        for _ in range(k):
                            lottery_pool.append(block["Validator"])
            lottery_winner = choice(lottery_pool)
            print(lottery_winner)
            for block in temp:
                if block["Validator"] == lottery_winner:
                    Blockchain.append(block)
                
                # write msg in announcement queue
                msg = '\n {0} 赢得了记账权利'.format(lottery_winner)
                await announcements.put(msg)
                break
        tempblocks.clear()


async def candidate(candidate_blocks):
    while True:
        try:
            candi = await candidate_blocks.get()
        except asyncio.QueueEmpty:
            await asyncio.sleep(1)
            pass
        tempblocks.append(candi)
    
async def run():
    t = str(datetime.now())
    genesis_block = {
        "Index": 0,
        "Timestamp": t,
        "BPM": 0,
        "PrevHash": "",
        "Validator": ""
    }

    genesis_block["Hash"] = caculate_hash(genesis_block)
    Blockchain.append(genesis_block)
    print(Blockchain)

    asyncio.ensure_future(candidate(candidate_blocks))
    asyncio.ensure_future(pick_winner(announcements))