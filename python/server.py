#!/bin/python2
import threading
import os
import socket
from multiprocessing import Process, Manager
from sock import Sock
from disk import Disk, PartitionInfo
from remote_file_manager import RemoteFileManager
from config import Config
    
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

            #Check the disk info.
            if cmd_list[0] == 'disk':
                if mutex.acquire():
                    #Lock and process
                    file_manager.send_devicelist(self.client_sock)
                    mutex.release()
                pass

            #Check partition info
            elif cmd_list[0] == 'df':
                if mutex.acquire():
                    file_manager.send_basic_partitioninfo(self.client_sock)
                    mutex.release()

            #Get file
            elif cmd_list[0] == 'get':
                file_manager.send_file(self.client_sock, cmd_list)

            #Enter a given directory
            elif cmd_list[0] == 'cd':
                file_manager.cd(self.client_sock, cmd_list)

            #Return the current directory
            elif cmd_list[0] == 'pwd':
                file_manager.send_current_directory(self.client_sock)

            #List files and directories
            elif cmd_list[0] == 'ls':
                if len(cmd_list) > 1:
                    file_manager.send_filelist(self.client_sock, cmd_list[1])
                else:
                    file_manager.send_currentfilelist(self.client_sock)

            #Shutdown the sever
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
    server_socket.bind(('',int(Config.get("SERVER_PORT")))) #Bind address and port
    server_socket.listen(5) #Listen 

    while True: #Loop
        (client_socket, address) = server_socket.accept() #When server accept a client
        print address
        ctthread = ClientThread(client_socket, address, status)   #Init a thread
        ctthread.start() #Start a thread

def broadcast(status):
        msg = Sock.get_ip_addr(Config.get("NETWORK_INTERFACE"))
        print msg
        destination = (Config.get("BROADCAST_ADDRESS"),int(Config.get("BROADCAST_PORT")))
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)

        while True:
            if status.value == False:
                print "Running status:"+str(status.value)
                break

            s.sendto(msg, destination)

def main():
    global file_manager
    global mutex
    global is_running

    manager = Manager()                     #Manager helps to handle shared variables between the process
    file_manager = RemoteFileManager() 
    mutex = threading.Lock()                #Create a threading Lock
    is_running = manager.Value('b', True)   #Shared process running state
    
    server_broadcast = Process(target=broadcast, args=(is_running,))
    server = Process(target=start_server, args=(is_running,))

    server_broadcast.start()                #Start broadcasting
    server.start()                          #Start server
    server_broadcast.join()
    server.join()

    
if __name__ == '__main__':
    main()
