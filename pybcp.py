#!/usr/bin/env python

import sys
import os
import time
from socket import *

BROADCAST_PORT = 4950
BCP_CODE = 3141593
BCP_TCP_PORT = 10789
BUF_SIZE = 2048

def sendBroadcast():
    udpsock = socket(AF_INET, SOCK_DGRAM)
    udpsock.setsockopt(SOL_SOCKET, SO_BROADCAST,1)
    s = str(BCP_CODE) + ' ' + str(BCP_TCP_PORT)
    buf = bytearray(s) + bytearray(BUF_SIZE - len(s))
    udpsock.sendto(str(buf), ('<broadcast>', BROADCAST_PORT))
    udpsock.close()

def recvBroadcast():
    udpsock = socket(AF_INET, SOCK_DGRAM)
    udpsock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) 
    udpsock.setsockopt(SOL_SOCKET, SO_BROADCAST,1)
    udpsock.bind(('', BROADCAST_PORT))
    msg, addr = udpsock.recvfrom(BUF_SIZE)
    msg = msg.rstrip('\0')
    code, port = msg.split(' ')
    code = int(code)
    port = int(port)
    ip = addr[0]
    return (ip, port)

def sendfile(filename, addr):
    tcpsock = socket(AF_INET, SOCK_STREAM)
    tcpsock.connect(addr)
    buf = bytearray(BUF_SIZE)
    f = open(filename, 'rb')
    filesize = os.path.getsize(filename)
    filepath, filename = os.path.split(filename)
    s = str(filename) + ' ' + str(filesize)
    array = bytearray(s) + bytearray(BUF_SIZE - len(s))
    tcpsock.sendall(array)
    while len(array) !=0:
        array = f.read(BUF_SIZE)
        tcpsock.sendall(array)
    tcpsock.close()

def recvfile():
    tcpsock = socket(AF_INET, SOCK_STREAM)
    tcpsock.bind(('', BCP_TCP_PORT))
    tcpsock.listen(1);
    conn, addr = tcpsock.accept()
    array = bytearray()
    i = 0
    while i!=BUF_SIZE:
        tmp = conn.recv(BUF_SIZE - i)
        array = array + tmp
        i = i + len(tmp)
    filename, filesize = str(array).split(' ')
    filesize = int(filesize.rstrip('\0'))
    f = open(filename+'test_new', 'wb')
    i = 0
    while i!=filesize:
        buf = conn.recv(BUF_SIZE)
        i = i + len(buf)
        f.write(buf)
    f.close()
    conn.close()
    tcpsock.close()
    
if len(sys.argv) > 1:
    addr = recvBroadcast()
    sendfile(sys.argv[1], addr)
else:
    sendBroadcast()
    recvfile()
