#!/usr/bin/env python3

import sys
import argparse
import websocket
from orderbook import OrderBook

DEFAULT_TICKER_SYMBOL='btcusd'
DEPTH_PERCENT_DEFAULT=0.01

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

orderBook = OrderBook(args.depthPercent)

def on_message(ws, message):
    #sys.stderr.write( message )
    orderBook.parseData( message )
    print( orderBook.toJson() )
    #orderBook.printStats()

ws = websocket.WebSocketApp(
    "wss://api.gemini.com/v1/marketdata/" + args.ticker,
    on_message=on_message)

ws.run_forever(ping_interval=5)

