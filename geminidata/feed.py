###
# Author: Riley Raschke <rileyATrrappsdevDOTcom>
# © 2019 rrappsdev.com
##

import sys
import socket

from json.decoder import JSONDecodeError
from websocket import create_connection
from websocket._exceptions import WebSocketConnectionClosedException
from threading import Thread
from threading import currentThread

from geminidata.service.exception import ServiceExit

class Feed:
    def __init__(self, feed_uri, ticker, onMessage):
        #self.feedSrcUris = []
        self.threads=[]
        self.feeds=[]
        self.feedUri = feed_uri
        self.onMessage = onMessage
        self.ticker = ticker
        #for feedUri in feedSrcUris:
        self._connect()

    def msg(self, message):
        self.onMessage( message, self.ticker)

    def _connect(self):
        self.feeds.append(
            create_connection( self.feedUri + self.ticker, sockopt=((socket.IPPROTO_TCP, socket.TCP_NODELAY, 1),) )
        )

    def _reconnect(self):
        self.stop()
        self.threads=[]
        self.feeds=[]
        self._connect()
        self.start()

    def _feedStart(self, feed, arg):
        t = currentThread()
        while getattr(t, "do_run", True):
            try:
                self.msg(feed.recv());
            except JSONDecodeError as e:
                print(self.ticker, 'got JSONDecodeError!')
                ##
                # Pretty sure this is just junk when zapped
                pass
            except WebSocketConnectionClosedException as e:
                #print(self.ticker, '- wss:// closed; -  %e' % e)
                print(self.ticker, '- wss:// closed!')
                ##
                # Pretty sure this is just junk when zapped
                pass
            except Exception as e:
                #print(self.ticker, '- Exception sending/receiving message: %e' % e)
                print(self.ticker, '- Exception sending/receiving message')
                pass

        print(self.ticker, "feed Stopped");

    def start(self):
        #try:
        for feed in self.feeds:
            t = Thread(target=self._feedStart, args=(feed, "task",))
            self.threads.append(t)
            t.start()

        for thread in self.threads:
            thread.join()

        #except ServiceExit as e:
        #    print('Caught ServiceExit in Feed as: %e' % e)
        #    self.stop()
        #    pass


    def stop(self):
        for feed in self.feeds:
            feed.close();
        for thread in self.threads:
            if thread.isAlive():
                thread.do_run = False
            thread.join()

