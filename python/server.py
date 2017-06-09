#!/bin/python2
import threading
import os
import socket
from sock import Sock
from disk import Disk, PartitionInfo
from remote_file_manager import RemoteFileManager
    

class ClientThread(threading.Thread):
    def __init__(self, client_socket, client_addr):
        threading.Thread.__init__(self)
        self.client_addr = client_addr
        self.client_sock = Sock(client_socket)

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

            if cmd_list[0] == 'df':

                if mutex.acquire():
                    file_manager.send_basic_partitioninfo(self.client_sock)
                    mutex.release()

            if cmd_list[0]== 'get':

                file_manager.send_file(self.client_sock, cmd_list)

            if cmd_list[0]== 'cd':
                file_manager.cd(self.client_sock, cmd_list)



            if cmd_list[0] == 'pwd':

                file_manager.send_current_directory(self.client_sock)

            if cmd_list[0] == 'exit':
                os._exit(0)




        

    

    def run(self):
        

        while True:

            msg = self.client_sock.recv()
            
            self.parseCommand(msg)
            
            
        print self.client_addr[0]+':'+str(self.client_addr[1]) + ' disconnected'
        self.client_socket.close()

            



        

def start_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Init TCP socket

    server_socket.bind(('',13136)) #Bind address and port

    server_socket.listen(5) #Listen 

    global file_manager
    global mutex

    file_manager = RemoteFileManager()
    mutex = threading.Lock()



    while True: #Loop

        (client_socket, address) = server_socket.accept() #When server accept a client
        ctthread = ClientThread(client_socket, address)   #Init a thread
        ctthread.start() #Start a thread



    
def main():
    start_server()

    
if __name__ == '__main__':
    main()
