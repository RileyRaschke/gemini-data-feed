###
# Author: Riley Raschke <rileyATrrappsdevDOTcom>
# © 2019 rrappsdev.com
##

import os
import socket
from threading import Thread
from threading import currentThread

class Broadcast:
    def __init__(self, socketPath ):
        #print( "Broadcast.__init__(BEGIN)" )
        self.serverRunning = False;
        self.socketPath = socketPath
        self.rebind()
        print("Created socket: " + self.socketPath)
        self.threads = []
        self.clients = []
        self.startServer()
        print( "Server broadcasting at: " + self.socketPath)

    def __del__(self):
        self.serverRunning = False
        self.stopServer()

    def rebind(self):
        self.sock = socket.socket( socket.AF_UNIX, socket.SOCK_STREAM )
        self.sock.settimeout(0.32)
        try:
            if os.access(self.socketPath, os.W_OK ):
                os.unlink(self.socketPath)
            self.sock.bind( self.socketPath )
            self.sock.listen(1)
        except Exception as e:
            print( "Failed to create socket: %s" % e )

    def clientHandler(self, arg):
        t = currentThread()
        while getattr(t, "do_run", True):
            try:
                c, addr = self.sock.accept()
                self.clients.append( (c,addr) )
                print ("Client connected");
                self.maintainClients();
                #print( "\nClient Count: " + str(len(self.clients)) + "; Thread Count: " + str(len(self.threads)) + "\n" )
            except Exception as e:
                pass
        print( "Server Listener Stopped");

    def startServer(self):
        if( len(self.threads) < 1 ):
            print("Starting New Listener")
            t = Thread(target=self.clientHandler, args=("task",))
            self.threads.append(t)
            t.start()
            self.serverRunning = True

    def stopServer(self):
        try:
            map( lambda x: x[0].close(), self.clients)
            self.sock.close()
            for thread in self.threads:
                if thread.isAlive():
                    thread.do_run = False
                thread.join()
            self.serverRunning = False
        except Exception as e:
            if( self.serverRunning == True ):
                self.serverRunning = False
                print( "Server mabye stopped with error: %s" % e )
                print( "Trying again!" )
                self.stopServer();

    def sendOrRelease( self, client, message ):
        try:
            if( client ):
                client[0].sendall( message.encode() )
            return True;
        except Exception as e:
            print( "Client disconnected: %s" % e )
            client[0].close()
            return False;

    def stats(self):
        print( "\nClient Count: " + str(len(self.clients)) + "; Thread Count: " + str(len(self.threads)) + "\n" )

    def emit( self, message ):
        try:
            if( len(self.clients) > 0 ):
                self.clients = list(filter(lambda x: self.sendOrRelease( x, message ), self.clients))

        except Exception as e:
            print( "Error occured, closing all clients and restarting server, e: %s" % e );
            map( lambda x: x[0].close(), self.clients)
            self.clients = []
            self.sock.close()
            self.rebind();

    def maintainClients( self ):
        try:
            self.threads = list(filter(lambda x: x.isAlive(), self.threads))
            self.startServer();
        except Exception as e:
            print("No clients to maintain: %s" % e)

