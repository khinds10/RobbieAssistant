#!/usr/bin/env python3
""" Consume new pushes in an asyncio for loop """
import asyncio
import sys, time, subprocess, json
import urllib
import logging
import threading
from functools import partial
from asyncpushbullet import AsyncPushbullet
from asyncpushbullet.async_listeners import WebsocketListener

# your API Key from PushBullet.com
API_KEY = "PUSH BULLET API KEY"

# dashboard central server host
dashboardServer = 'my.server.com'

def logException(exception):
    """ print the exception to standard output for debugging """
    return
    if hasattr(exception, 'message'):
        print(exception.message)
    else:
        print(exception)
    print(type(exception).__name__)
    print(exception.__class__.__name__)

def httpPOSTMessage(message):
    """  POST via HTTP the parsed message to dashboard server """
    message = message.replace('\n', ' ')
    req = urllib.request.Request('http://'+dashboardServer+'/message/set', data=message.encode("utf-8"),headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(req)    

def pushMessage(message):
    """ push the message the dashboard server """
    
    # get standard notification
    try:
        httpPOSTMessage(message['push']['title'][0:50] + ' - ' + message['push']['body'][0:200] + '...')
        return
    except Exception as exception:
        if message['type'] != 'nop':   
            logException(exception)

    # get SMS notification
    try:
        httpPOSTMessage(message['push']['notifications'][0]['title'][0:50] + ' - ' + message['push']['notifications'][0]['body'][0:200] + '...')
    except Exception as exception:
        if message['type'] != 'nop':          
            logException(exception)
        
async def ws_connected(listener: WebsocketListener):
    print("Connected to websocket")

async def ws_msg_received(ws_msg: dict, listener: WebsocketListener):
    pushMessage(ws_msg)

async def ws_closed(listener: WebsocketListener):
    print("ws_closed")

def run():
    """ Uses a callback scheduled on an event loop"""
    pb = AsyncPushbullet(API_KEY)
    listener = WebsocketListener(pb, on_connect=ws_connected,on_message=ws_msg_received,on_close=ws_closed)
    loop = asyncio.get_event_loop()
  
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        print("finally...")
        loop.run_until_complete(listener.close())
        loop.run_until_complete(pb.close())
  
# let's run the main loop and listen for phone notifications
if __name__ == '__main__':
    run()
