#!/usr/bin/env python3
# -*- coding:utf-8 -*- 

"""
This module is a simple block generate logic 
"""
from hashlib import sha256
from datetime import datetime

def generate_block(old_block, bpm, address):
    """
    :params oldblock
    :params bpm
    :params address
    :return
    """

    new_block = {
        "Index": old_block["Index"] + 1,
        "BPM": bpm,
        "Timestamp": str(datetime.now()),
        "PrevHash": old_block["Hash"],
        "Validator": address
    }

    new_block["Hash"] = caculate_hash(new_block) 
    return new_block

def caculate_hash(block):
    """
    calcuate block sha256 hash value
    """
    record  = "".join([
        str(block["Index"]),
        str(block["BPM"]),
        block["Timestamp"],
        block["PrevHash"]
    ])
    return sha256(record.encode()).hexdigest()


def is_block_valid(new_block, old_block):
    """
    simple verify if the block is valid.
    """
    if old_block["Index"] + 1 != new_block["Index"]:
        return False
    
    if old_block["Hash"] != new_block["PrevHash"]:
        return False
    
    if caculate_hash(new_block) != new_block["Hash"]:
        return False
    
    return True