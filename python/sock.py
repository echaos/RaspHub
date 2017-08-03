#!/bin/python2
import struct
import socket
import fcntl

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
    def get_ip_addr(name):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', name[:15])
        )[20:24])
        

