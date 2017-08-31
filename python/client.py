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
    s.connect(('127.0.0.1', 13135))

    sock = Sock(s)

    while True:
        cmd = raw_input('$:')
        cmd_list = cmd.split()
        cmd_len = len(cmd_list)

        if cmd == 'disk':
            sock.send('disk')
            feedback(sock)

        if cmd == 'df':
            sock.send('df')
            feedback(sock)

        if cmd_list[0] == 'get':
            if cmd_len == 2:
                sock.send('get '+cmd_list[1])
                feedback(sock)
            else:
                print 'Invalid input'

        if cmd == 'pwd':
            sock.send(cmd)
            print sock.recv()

        if cmd.split()[0] == 'cd':
            if cmd_len == 2:
                sock.send('cd '+cmd_list[1])
                feedback(sock)
            else:
                print 'Invalid input'


        if cmd.split()[0] == 'ls':
            if cmd_len == 2:
                sock.send('ls '+cmd_list[1])
                feedback(sock)
            elif cmd_len == 1:
                sock.send('ls')
                feedback(sock)
            else:
                print 'Invalid input'

        if cmd == 'shutdown':
            sock.send('shutdown')

        if cmd == 'exit':
            break
            
    s.close()

if __name__ == '__main__':
    main()
