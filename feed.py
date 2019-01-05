#!/usr/bin/env python3

import sys
import os,tempfile
import socket
import argparse
import websocket
from pathlib import Path
from orderbook import OrderBook

DEPTH_PERCENT_DEFAULT=0.01
DEFAULT_TICKER_SYMBOL='btcusd'
DEFAULT_SOCKET_PREFIX = '/tmp/gemini-'
DEFAULT_SOCKET= ''.join([DEFAULT_SOCKET_PREFIX,DEFAULT_TICKER_SYMBOL,".sock"])
namedPipe = ""

opts = argparse.ArgumentParser(description="Display Gemini data feed in terminal.")

opts.add_argument(
    '-t', '--ticker',
    default=DEFAULT_TICKER_SYMBOL,
    help='Ticker string. ex: btcusd ethbtc bchusd'
)
opts.add_argument(
    '-d', '--depthPercent',
    type=float,
    default=DEPTH_PERCENT_DEFAULT,
    help='Ticker string. ex: btcusd ethbtc bchusd'
)

args = opts.parse_args()

if( args.ticker ):
    namedPipe = ''.join([DEFAULT_SOCKET_PREFIX,args.ticker,".sock"])

if os.access(namedPipe, os.W_OK ):
    os.unlink(namedPipe)

tmpDir = tempfile.mkdtemp()
filename = os.path.join(tmpDir,namedPipe)

#try:
#    os.mkfifo(filename)
#except OSError as e:
#    print( "Failed to create FIFO: %s" % e )
#else:
#    fifo = open( filename, 'w')

#s = socket.socket(socket.AF_UNIX)
#s.settimeout(1)
#try:
#    s.connect(namedPipe)
#except Exception:
#    Path(namedPipe).touch()
#    s.connect(namedPipe)
def writePipe( message ):
    print( message, file=fifo)

orderBook = OrderBook(args.depthPercent)
def on_message(ws, message):
    #sys.stderr.write( message )
    orderBook.parseData( message )
    #writePipe( orderBook.toJson() );
    print( orderBook.toJson() );
    #orderBook.printStats()

ws = websocket.WebSocketApp(
    "wss://api.gemini.com/v1/marketdata/" + args.ticker,
    on_message=on_message)

ws.run_forever(ping_interval=5)

