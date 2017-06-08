import struct

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

