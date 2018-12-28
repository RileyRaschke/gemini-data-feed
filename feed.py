#!/usr/bin/env python3

import traceback
import pprint

import websocket
import json

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
            self.last = event['price']
            self.lastSide = event['makerSide']
            self.lastAmount = event['amount']

        if event['type'] == 'change':
            try:
                if event['side'] == 'bid':
                    if not str(event['price']) in self.bidBook:
                        self.bidBook[str(event['price'])] = 0.0
                    self.bidBook[str(event['price'])] += float(event['delta'])
                elif event['side'] == 'ask':
                    if not str(event['price']) in self.askBook:
                        self.askBook[str(event['price'])] = 0.0
                    self.askBook[str(event['price'])] = float(event['delta'])
            except Exception:
                traceback.print_exc()

    def printStats(self):
        print(
            "Last: " + str(self.last) +
            " LastSide: " + self.lastSide +
            " LastAmount: " + str(self.lastAmount) + "\n"
        )
        print("BidBook: ")
        pprint.pprint( self.bidBook )
        print("AskBook: ")
        pprint.pprint( self.askBook )

orderBook = OrderBook()

def on_message(ws, message):
    feedData = json.loads( message );
    #if( feedData['events']
    #print( str(feedData['socket_sequence']) + " " + str(feedData['events']) )
    for event in feedData['events']:
        orderBook.addEvent( event )
        orderBook.printStats()

ws = websocket.WebSocketApp("wss://api.gemini.com/v1/marketdata/btcusd", on_message=on_message)

ws.run_forever(ping_interval=5)

