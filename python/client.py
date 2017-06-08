#!/bin/python2
import socket
from sock import *

def print_list(sock):
    n = int(sock.recv())

    sock.send('ok')

    for i in range(n):
        print len(sock.recv())
        print '|'
        print i
        print ''



def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 13136))

    sock = Sock(s)

    while True:
        cmd = raw_input('$:')

        if cmd == 'disk':
            sock.send('disk')
            print_list(sock)

        if cmd.split()[0] == 'get':
            sock.send('get'+cmd.split()[1])
            print_list(sock)

        if cmd == 'exit':
            sock.send('exit')
            break
            
    s.close()

if __name__ == '__main__':
    main()
