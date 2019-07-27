###
# Author: Riley Raschke <rileyATrrappsdevDOTcom>
# © 2019 rrappsdev.com
##

import signal
from threading import Thread
from orderbook import OrderBook
from feed import Feed
from main import Broadcast
from exc import ServiceExit

class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass

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
            self.feeds[ticker] = Feed.Feed( self.feedUri, ticker, self.onMessage )
            self.orderbooks[ticker] = OrderBook.OrderBook( self.depthPercent[ticker], ticker )

        # Write stuff
        self.socket = Broadcast.Broadcast( self.outpipe )

    # Exit clean.
    def service_shutdown(self, signum, frame):
        print('Caught signal %d' % signum)
        #self.socket.stopServer()
        raise ServiceExit

    # Method is bound to each `Feed` during __init__()
    def onMessage(self, message, ticker):
        self.orderbooks[ticker].parseData( message )
        self.socket.emit( self.orderbooks[ticker].toJson() )
        #print( self.orderbooks[ticker].statsString() )
        #self.socket.emit( message )
        #print( message )

    def run( self ):
        #print( "Hello World!" );
        print( "Main.run()" )
        try:
            for ticker in self.tickers:
                t = Thread(target=self.feeds[ticker].start )
                self.threads[ticker] = t
                t.start()

            for ticker in self.tickers:
                self.threads[ticker].join()

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

