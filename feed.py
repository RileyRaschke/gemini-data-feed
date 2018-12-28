#!/usr/bin/env python3

DEFAULT_TICKER_SYMBOL='btcusd'

import traceback
import pprint

import websocket
import json

import argparse
opts = argparse.ArgumentParser(description="Display Gemini data feed in terminal.")
opts.add_argument('-t', '--ticker', default=DEFAULT_TICKER_SYMBOL, help='Ticker string. ex: btcusd ethbtc bchusd')
args = opts.parse_args()

class OrderBook:
    def __init__(self):
        self.bidBook = {}
        self.askBook = {}
        self.last = 0.0
        self.lastSide = ""
        self.lastAmount = 0.0
        self.bid = 0.0
        self.bidSize = 0.0
        self.ask = 0.0
        self.askSize = 0.0

    def addEvent(self, event):
        if event['type'] == 'trade':
            self.last = float(event['price'])
            self.lastAmount = float(event['amount'])
            self.lastSide = event['makerSide']

        if event['type'] == 'change':
            try:

                if event['side'] == 'bid':
                    if not str(event['price']) in self.bidBook:
                        self.bidBook[str(event['price'])] = 0.0
                    self.bidBook[str(event['price'])] += float(event['delta'])
                elif event['side'] == 'ask':
                    if not str(event['price']) in self.askBook:
                        self.askBook[str(event['price'])] = 0.0
                    self.askBook[str(event['price'])] += float(event['delta'])

                if self.bidBook:
                    self.bid = max( map(lambda x: float(x), dict(filter(lambda x: x[1] > 0, self.bidBook.items())).keys()) );
                    if self.bid > 0: self.bidSize = self.bidBook[ "{:5.2f}".format(self.bid) ]
                if self.askBook:
                    self.ask = min( map(lambda x: float(x), dict(filter(lambda x: x[1] > 0, self.askBook.items())).keys()) );
                    if self.ask > 0: self.askSize = self.askBook[ "{:5.2f}".format(self.ask) ]

            except Exception:
                traceback.print_exc()

    def printLast(self):
        print(
            "Last: " + str(self.last) +
            " spread: " + str(self.ask-self.bid) +
            " last_amt: " + str(self.lastAmount) +
            " last_side: " + self.lastSide
        )

    def printStats(self):
        try:
            pprint.pprint( dict(filter( lambda x: float(x[0]) > self.bid-7.5 and x[1] > 0, self.bidBook.items() )) )
            print( "bid: " + str(self.bid) + "x" + str(self.bidSize) )

            if self.last > 0: self.printLast()
            else: print("spread: " + str(self.ask-self.bid) )

            print( "ask: " + str(self.ask) + "x" + str(self.askSize) )
            pprint.pprint( dict(filter( lambda x: float(x[0]) < self.ask+7.5 and x[1] > 0, self.askBook.items() )) )
            print("\n")
        except Exception:
            traceback.print_exc()

orderBook = OrderBook()

def on_message(ws, message):
    feedData = json.loads( message );
    #if( feedData['events']
    #print( str(feedData['socket_sequence']) + " " + str(feedData['events']) )
    for event in feedData['events']:
        orderBook.addEvent( event )
        orderBook.printStats()

ws = websocket.WebSocketApp("wss://api.gemini.com/v1/marketdata/" + args.ticker, on_message=on_message)

ws.run_forever(ping_interval=5)

