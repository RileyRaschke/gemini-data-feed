#!/usr/bin/python3 -u

import sys
import os
import socket
import time

SOCKET_PATH = '/tmp/test_socket.sock'

if os.access(SOCKET_PATH, os.W_OK ):
    os.unlink(SOCKET_PATH)

with socket.socket( socket.AF_UNIX, socket.SOCK_STREAM ) as s:
    s.bind( SOCKET_PATH )
    s.listen(5)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr )
        while True:
            data = "{:5.0f}".format(time.time()) + "\n";
            conn.sendall( data.encode() )
            time.sleep(1)

