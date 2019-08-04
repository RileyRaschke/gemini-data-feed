###
# Author: Riley Raschke <rileyATrrappsdevDOTcom>
# © 2019 rrappsdev.com
##

import sys
import traceback
import time
import json
import pprint

from functools import reduce
from datetime import datetime

class OrderBook:
    def __init__(self, depthPercent, ticker):
        self.ticker = ticker
        self.depthPercent = depthPercent
        self.bidBook = {}
        self.askBook = {}
        self.bidDepth = {}
        self.askDepth = {}
        self.last = 0.0
        self.lastSide = ""
        self.lastAmount = 0.0
        self.lastTickTS = 0
        self.bid = 0.0
        self.bidTs = 0
        self.bidSize = 0.0
        self.bidDepthSize = 0.0
        self.ask = 0.0
        self.askTs = 0
        self.askSize = 0.0
        self.askDepthSize = 0.0
        self.lastSeqNo = -1

    def parseData( self, message):
        feedData = json.loads( message )
        ts = 0
        if 'timestamp' in feedData.keys(): ts = feedData['timestamp']
        else: ts = int(time.time())

        if 'socket_sequence' in feedData.keys() and feedData['socket_sequence'] > self.lastSeqNo:
            self.lastSeqNo = feedData['socket_sequence']
            for event in feedData['events']:
                self.addEvent( event, ts )
            #self.printStats()
            #print( self.toJson() )
        else:
            sys.stderr.write( "Socket message out of sequence - discarded:" )
            sys.stderr.write( message )


    def addEvent(self, event, timestamp):
        if event['type'] == 'trade':
            self.last = float(event['price'])
            self.lastAmount = float(event['amount'])
            self.lastSide = event['makerSide']
            self.lastTickTS = int(timestamp)

        if event['type'] == 'change':
            try:
                if event['side'] == 'bid':
                    if not str(event['price']) in self.bidBook:
                        self.bidBook[ "{:5.2f}".format(float(event['price'])) ] = 0.0
                    self.bidBook[ "{:5.2f}".format(float(event['price'])) ] += float(event['delta'])
                elif event['side'] == 'ask':
                    if not str(event['price']) in self.askBook:
                        self.askBook[ "{:5.2f}".format(float(event['price'])) ] = 0.0
                    self.askBook[ "{:5.2f}".format(float(event['price'])) ] += float(event['delta'])

                if self.bidBook:
                    viableBids = dict(filter(lambda x: x[1] > 0.00001, self.bidBook.items()))
                    if viableBids:
                        self.bid = max( map(lambda x: float(x), viableBids.keys()) );
                        if self.bid > 0.00001:
                            self.bidSize = self.bidBook[ "{:5.2f}".format(self.bid) ]
                            self.bidTs = int(timestamp)

                        self.bidDepth = dict( filter(
                            lambda x:
                                float(x[0]) > self.bid - self.bid*self.depthPercent,
                            viableBids.items()
                        ))
                        self.bidDepthSize = reduce( lambda x, y: x+y, self.bidDepth.values() );

                if self.askBook:
                    viableAsks = dict(filter(lambda x: x[1] > 0.00001, self.askBook.items()))
                    if viableAsks:
                        self.ask = min( map(lambda x: float(x), viableAsks.keys()) );
                        if self.ask > 0.00001:
                            self.askSize = self.askBook[ "{:5.2f}".format(self.ask) ]
                            self.askTs = int(timestamp)

                        self.askDepth = dict( filter(
                            lambda x:
                                float(x[0]) < self.ask + self.ask*self.depthPercent,
                            viableAsks.items()
                        ))
                        self.askDepthSize = reduce( lambda x, y: x+y, self.askDepth.values() );

            except Exception:
                traceback.print_exc()

    def lastPriceString(self):
        return (
            "Last: " + "{:5.2f}".format(self.last) +
            " x " + "{:5.5f}".format(self.lastAmount) +
            "; last_side: " + self.lastSide +
            "; spread: " + "{:5.5f}".format(self.ask-self.bid) +
            "; " + datetime.utcfromtimestamp(self.lastTickTS).strftime('%H:%M:%S') +
            "; seq: " + str(self.lastSeqNo)
        )

    def statsString(self):
        res = "";
        try:
            #res += pprint.pformat( self.bidDepth ) + "\n"
            res += "bidDepth: " + "{:5.1f}".format(self.bidDepthSize) + "\n"
            res += "bid: " + "{:5.2f}".format(self.bid) + " x " + "{:5.5f}".format(self.bidSize)
            res += " @ " + datetime.utcfromtimestamp(self.bidTs).strftime('%H:%M:%S') + "\n"

            if self.last > 0:
                res += self.lastPriceString() + "\n"
            else:
                res += "spread: " + "{:5.5f}".format(self.ask-self.bid)
                res += "; seq: " + str(self.lastSeqNo) + "\n"

            res += "ask: " + "{:5.2f}".format(self.ask) + " x " + "{:5.5f}".format(self.askSize)
            res += " @ " + datetime.utcfromtimestamp(self.askTs).strftime('%H:%M:%S') + "\n"
            res += "askDepth: " + "{:5.1f}".format(self.askDepthSize)
            #res += "\n" + pprint.pformat( self.askDepth ) + "\n"
        except Exception:
            traceback.print_exc()

        return res

    def toJson(self):
        try:
            return json.dumps(
                dict(filter( lambda x: x[0] not in ('bidBook','askBook'), self.__dict__.items() )),
                sort_keys=True, indent=2
            )
        except Exception:
            traceback.print_exc()

