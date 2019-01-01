
import sys
import traceback
import time
import json
import pprint
from functools import reduce
from datetime import datetime

class OrderBook:
    def __init__(self, depthPercent):
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

            self.printStats()
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

    def printLast(self):
        print(
            "Last: " + "{:5.2f}".format(self.last) +
            " x " + "{:5.5f}".format(self.lastAmount) +
            "; last_side: " + self.lastSide +
            "; spread: " + "{:5.5f}".format(self.ask-self.bid) +
            "; " + datetime.utcfromtimestamp(self.lastTickTS).strftime('%H:%M:%S')
        )

    def printStats(self):
        try:
            pprint.pprint( self.bidDepth );
            print( "bidDepth: " + "{:5.1f}".format(self.bidDepthSize) )
            print( "bid: " + "{:5.2f}".format(self.bid) + " x " + "{:5.5f}".format(self.bidSize)
                +" @ " + datetime.utcfromtimestamp(self.bidTs).strftime('%H:%M:%S')
            )

            if self.last > 0: self.printLast()
            else: print("spread: " + "{:5.5f}".format(self.ask-self.bid) )

            print( "ask: " + "{:5.2f}".format(self.ask) + " x " + "{:5.5f}".format(self.askSize)
                + " @ " + datetime.utcfromtimestamp(self.askTs).strftime('%H:%M:%S')
            )
            print( "askDepth: " + "{:5.1f}".format(self.askDepthSize) )
            pprint.pprint( self.askDepth );
        except Exception:
            traceback.print_exc()


