#!/bin/python2
import socket
from sock import *

def feedback(sock):
    n = int(sock.recv())

    if n == 0:
        print sock.recv()

    elif n > 0:

        sock.send('ok')

        for i in range(n):
            print sock.recv()

    else:
        print 'Error'
        print sock.recv() # Receive message



def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 13136))

    sock = Sock(s)

    while True:
        cmd = raw_input('$:')

        if cmd == 'disk':
            sock.send('disk')
            feedback(sock)

        if cmd == 'df':
            sock.send('df')
            feedback(sock)

        if cmd.split()[0] == 'get':
            sock.send('get '+cmd.split()[1])
            feedback(sock)

        if cmd == 'pwd':
            sock.send(cmd)
            print sock.recv()

        if cmd.split()[0] == 'cd':
            sock.send('cd '+cmd.split()[1])
            feedback(sock)

        if cmd == 'exit':
            sock.send('exit')
            break
            
    s.close()

if __name__ == '__main__':
    main()
