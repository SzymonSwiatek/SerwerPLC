#!/usr/bin/env python

# WS server example

import asyncio
import datetime
import random
import websockets
import json
import plc
import snap7
from snap7.util import *
from snap7.snap7types import *

myplc = snap7.client.Client()
plc_IP = '192.168.10.56'
plc_RACK = 0
plc_SLOT = 1

try:
    myplc.connect(plc_IP, plc_RACK, plc_SLOT)
except ConnectionError:
    print("Upss...")


def consumer(message):
    data = json.loads(message)
    print(" ")
    #print(data)
    if data['M00']:
        plc.set_merkers(myplc, 0, 0, S7WLBit,1)
        print("M0.0 = 1")
    else:
        plc.set_merkers(myplc, 0, 0, S7WLBit, 0)
        print("M0.0 = 0")
        
    if data['M01']:
        plc.set_merkers(myplc, 0, 1,S7WLBit , 1)
        print("M0.1 = 1")
    else:
        plc.set_merkers(myplc, 0, 1, S7WLBit, 0)
        print("M0.1 = 0")
        
    if data['M02']:
        plc.set_merkers(myplc, 0, 2, S7WLBit,1)
        print("M0.2 = 1")
    else:
        plc.set_merkers(myplc, 0, 2, S7WLBit, 0)
        print("M0.2 = 0")
        
    if data['M03']:
        plc.set_merkers(myplc, 0, 3, S7WLBit, 1)
        print("M0.3 = 1")
    else:
        plc.set_merkers(myplc, 0, 3, S7WLBit, 0)
        print("M0.3 = 0")
        
    if data['M04']:
        plc.set_merkers(myplc, 0, 4, S7WLBit, 1)
        print("M0.4 = 1")
    else:
        plc.set_merkers(myplc, 0, 4, S7WLBit, 0)
        print("M0.4 = 0")
        
    if data['M05']:
        plc.set_merkers(myplc, 0, 5, S7WLBit, 1)
        print("M0.5 = 1")
    else:
        plc.set_merkers(myplc, 0, 5, S7WLBit, 0)
        print("M0.5 = 0")
        
    if data['M06']:
        plc.set_merkers(myplc, 0, 6, S7WLBit, 1)
        print("M0.6 = 1")
    else:
        plc.set_merkers(myplc, 0, 6, S7WLBit, 0)
        print("M0.6 = 0")
        
    if data['M07']:
        plc.set_merkers(myplc, 0, 7, S7WLBit, 1)
        print("M0.7 = 1")
    else:
        plc.set_merkers(myplc, 0, 7, S7WLBit, 0)
        print("M0.7 = 0")

async def producer():
    STATE = {
        "Connected":  myplc.get_connected(),
        "Q0": plc.get_process_outputs_bit(myplc, 0, 0),
        "Q1": plc.get_process_outputs_bit(myplc, 0, 1),
        "Q2": plc.get_process_outputs_bit(myplc, 0, 2),
        "Q3": plc.get_process_outputs_bit(myplc, 0, 3),
        "Q4": plc.get_process_outputs_bit(myplc, 0, 4),
        "Q5": plc.get_process_outputs_bit(myplc, 0, 5),
        "M10": plc.get_merkers(myplc, 1, 0, S7WLBit),
        "M13": plc.get_merkers(myplc, 1, 3, S7WLBit),
        "I0": plc.get_process_inputs_bit(myplc, 0, 0),
        "I1": plc.get_process_inputs_bit(myplc, 0, 1),
        "I2": plc.get_process_inputs_bit(myplc, 0, 2),
        "I3": plc.get_process_inputs_bit(myplc, 0, 3),
        "I4": plc.get_process_inputs_bit(myplc, 0, 4),
        "I5": plc.get_process_inputs_bit(myplc, 0, 5),
        "I6": plc.get_process_inputs_bit(myplc, 0, 6),
        "I7": plc.get_process_inputs_bit(myplc, 0, 7),
    }
    return json.dumps({**STATE})


async def consumer_handler(websocket, path):
    async for message in websocket:
        consumer(message)


async def producer_handler(websocket, path):
    while True:
        message = await producer()
        await websocket.send(message)
        await asyncio.sleep(1)


async def handler(websocket, path):
    consumer_task = asyncio.ensure_future(
        consumer_handler(websocket, path))
    producer_task = asyncio.ensure_future(
        producer_handler(websocket, path))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()


start_server = websockets.serve(handler, "192.168.1.16", 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
