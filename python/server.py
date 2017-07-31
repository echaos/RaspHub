#!/bin/python2
import threading
import os
import socket
from multiprocessing import Process, Manager
from sock import Sock
from disk import Disk, PartitionInfo
from remote_file_manager import RemoteFileManager
    
class ClientThread(threading.Thread):
    def __init__(self, client_socket, client_addr, status):
        threading.Thread.__init__(self)
        self.client_addr = client_addr
        self.client_sock = Sock(client_socket)
        self.status = status

    def parseCommand(self,line):
        if line:
            print line
            cmd_list = line.split()
            print cmd_list[0]

            if cmd_list[0] == 'disk':
                #Check the disk info.
                if mutex.acquire():
                    file_manager.send_devicelist(self.client_sock)
                    mutex.release()

                
                pass

            elif cmd_list[0] == 'df':
                if mutex.acquire():
                    file_manager.send_basic_partitioninfo(self.client_sock)
                    mutex.release()

            elif cmd_list[0] == 'get':
                file_manager.send_file(self.client_sock, cmd_list)

            elif cmd_list[0] == 'cd':
                file_manager.cd(self.client_sock, cmd_list)

            elif cmd_list[0] == 'pwd':
                file_manager.send_current_directory(self.client_sock)

            elif cmd_list[0] == 'ls':
                if len(cmd_list) > 1:
                    file_manager.send_filelist(self.client_sock, cmd_list[1])
                else:
                    file_manager.send_currentfilelist(self.client_sock)

            elif cmd_list[0] == 'exit':
                self.status.value = False
                os._exit(0)

            else:
                pass

    def run(self):
        

        while True:
            msg = self.client_sock.recv()
            self.parseCommand(msg)
            
        print self.client_addr[0]+':'+str(self.client_addr[1]) + ' disconnected'
        self.client_socket.close()

def start_server(status):
    print 'Server started.'
    
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Init TCP socket
    server_socket.bind(('',13136)) #Bind address and port
    server_socket.listen(5) #Listen 



    while True: #Loop
        (client_socket, address) = server_socket.accept() #When server accept a client
        print address
        ctthread = ClientThread(client_socket, address, status)   #Init a thread
        ctthread.start() #Start a thread

def broadcast(status):
        msg = socket.gethostbyname(socket.gethostname())
        print msg
        destination = ('233.233.233.233',13135)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # s.bind(('',0))
        # s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)

        while True:
            
            if status.value == False:
                print "Running status:"+str(status.value)
                break

            s.sendto(msg, destination)
#             (buf, address) = s.recvfrom(10100)
            # if not len(buff):
                # break


def main():
    global file_manager
    global mutex
    global is_running
    manager = Manager()

    file_manager = RemoteFileManager() 
    mutex = threading.Lock()                #Lock
    is_running = manager.Value('b', True)   #Shared process running state
    
    server_broadcast = Process(target=broadcast, args=(is_running,))
    server = Process(target=start_server, args=(is_running,))
    server_broadcast.start()
    server.start()

    server_broadcast.join()
    server.join()

    
if __name__ == '__main__':
    main()
