###
# Author: Riley Raschke <rileyATrrappsdevDOTcom>
# © 2019 rrappsdev.com
##

import time
import signal
from threading import Thread

from geminidata import OrderBook, Feed

from .exception import ServiceExit
from .broadcast import Broadcast

class Main:
    def __init__(self, feedUri, tickerDepths, outpipe):
        # Bind to control signals
        signal.signal(signal.SIGTERM, self.service_shutdown)
        signal.signal(signal.SIGINT, self.service_shutdown)

        # init provided internals
        self.feedUri   = feedUri
        self.tickers   = tickerDepths.keys()
        self.outpipe = outpipe
        self.depthPercent = tickerDepths

        # housekeeping
        self.feeds  = {}
        self.threads = {}
        self.orderbooks = {}

        # Build stuff
        for ticker in self.tickers:
            self.feeds[ticker] = Feed( self.feedUri, ticker, self.onMessage )
            self.orderbooks[ticker] = OrderBook( self.depthPercent[ticker], ticker )

        # Write stuff
        self.socket = Broadcast( self.outpipe )

    # Exit clean.
    def service_shutdown(self, signum, frame):
        print('Caught signal %d' % signum)
        raise ServiceExit

    # Method is bound to each `Feed` during __init__()
    def onMessage(self, message, ticker):
        self.orderbooks[ticker].parseData( message )
        self.socket.emit( self.orderbooks[ticker].toJson() )
        #print( self.orderbooks[ticker].statsString() )
        #self.socket.emit( message )
        #print( message )

    def run( self ):
        try:
            for ticker in self.tickers:
                t = Thread(target=self.feeds[ticker].start )
                self.threads[ticker] = t
                t.start()

            for ticker in self.tickers:
                self.threads[ticker].join()
                time.sleep(5)
                t = Thread(target=self.feeds[ticker]._reconnect )
                self.threads[ticker] = t
                t.start()

            self.run() # foreverIsh!
        except ServiceExit:
            print("Stopping Service")

        for ticker in self.tickers:
            try:
                print("Stopping feed for:", ticker)
                self.feeds[ticker].stop()
            except Exception as e:
                print('Exception stoping feeds: %e' % e)

        print("Feeds Terminated.")
        print("Stopping local server.")
        self.socket.stopServer()
        print("server stopped")
        return 0

