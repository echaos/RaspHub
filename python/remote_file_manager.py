import os
import math
from config import Config
from sock import Sock
from disk import Disk, PartitionInfo

BUFFER_SIZE = 8192

class RemoteFileManager():


    def __init__(self):
        self._current_directory = Config.config().valueof('default_directory')
        self._last_directory = '..'+self._current_directory
        self._disk = Disk()

        pass

    def send_devicelist(self, client_sock):
        
        partition_list = self._disk.list_partitions()

        client_sock.send(str(len(partition_list)))

        if client_sock.recv() == 'ok':
            for name in partition_list:
                client_sock.send(self._disk.device(name))
                
    def send_basic_partitioninfo(self, client_sock):

        partition_list = self._disk.list_partitions()

        client_sock.send(str(len(partition_list)))

        if client_sock.recv() == 'ok':
            for name in partition_list:
                info = self._disk.partitioninfo(name)
                client_sock.send(info.name()+':'+info.size()+':'+info.label()+':'+info.mountpoint())

    def send_filelist(self, client_sock, path):
        #Add exception handling here
        filelist = os.listdir(path)
        client_sock.send(str(len(filelist))) #Send file number
        
        if client_sock.recv() == 'ok':

            for filename in filelist:
                client_sock.send(filename)

    def send_currentfilelist(self, client_sock):
        self.send_filelist(client_sock, self._current_directory)

    def cd(self, path):
        self._last_directory = self._current_directory
        self._current_directory = path



    def send_file(self, client_sock, filepath):
        f = open(filepath,'rb')
        
        #Add exception handling here
        file_size = os.path.getsize(filepath)

        #Send the while times
        client_sock.send(str(int(math.ceil(float(file_size)/float(BUFFER_SIZE)))))

        while True:
            buff = f.read(BUFFER_SIZE)
            if buff == '':
                break
            client_sock.send(buff)
    
    

    def current_directory(self):
        return _current_directory

    

