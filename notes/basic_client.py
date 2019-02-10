#!/usr/bin/python3 -u

import sys
import os
import socket
import time

SOCKET_PATH = '/tmp/test_socket.sock'

with socket.socket( socket.AF_UNIX, socket.SOCK_STREAM ) as s:
    s.connect( SOCKET_PATH )
    #s.sendall(b'Hello, world')
    while True:
        data = s.recv(1024)
        #print( 'Received ', data.decode );
        print( 'Received ',repr( data ) );

