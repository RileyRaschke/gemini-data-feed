###
# Author: Riley Raschke <rileyATrrappsdevDOTcom>
# © 2019 rrappsdev.com
##

import sys
#import websocket
import socket
from websocket import create_connection
from threading import Thread
from threading import currentThread

class Feed:
    def __init__(self, feed_uri, ticker, onMessage):
        #self.feedSrcUris = []
        self.threads=[]
        self.feeds=[]
        self.feedUri = feed_uri
        self.onMessage = onMessage
        self.ticker = ticker
        #for feedUri in feedSrcUris:
        self.feeds.append(
            create_connection( self.feedUri + ticker, sockopt=((socket.IPPROTO_TCP, socket.TCP_NODELAY, 1),) )
        )

    def msg(self, message):
        self.onMessage( message, self.ticker)

    def _feedStart(self, feed, arg):
        t = currentThread()
        while getattr(t, "do_run", True):
            try:
                self.msg(feed.recv());
            except Exception as e:
                pass
        print(self.ticker,"feed Stopped");

    def start(self):
        for feed in self.feeds:
            t = Thread(target=self._feedStart, args=(feed, "task",))
            self.threads.append(t)
            t.start()

        for thread in self.threads:
            thread.join();

    def stop(self):
        for feed in self.feeds:
            feed.close();
        for thread in self.threads:
            if thread.isAlive():
                thread.do_run = False
            thread.join()

