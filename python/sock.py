#!/bin/python2
import struct
import socket

class Sock():
    
    def __init__(self):
        pass

    def __init__(self, socket):
        self.socket = socket

    def send(self, msg):
        msg = struct.pack('>I', len(msg))+msg
        self.socket.sendall(msg)

    def recv(self):
        raw_msglen = self.recvall(4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        return self.recvall(msglen)

    def recvall(self,n):
        data = ''
        while len(data) < n:
            packet = self.socket.recv(n - len(data))
            if not packet:
                return None
            data += packet

        return data

    def senderr(self,e):
        self.send('-1')
        self.send(e.message)


    @staticmethod
    def broadcast():
        msg = socket.gethostbyname(socket.gethostname())
        print msg
        destination = ('233.233.233.233',13135)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # s.bind(('',0))
        # s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)


        while True:

            s.sendto(msg, destination)
#             (buf, address) = s.recvfrom(10100)
            # if not len(buff):
                # break

        
if __name__ == "__main__":
    Sock.broadcast()


