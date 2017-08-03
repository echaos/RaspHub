import os
import math
from config import Config
from sock import Sock
from disk import Disk, PartitionInfo

BUFFER_SIZE = 8192

class RemoteFileManager():

    def __init__(self):
        self._current_directory = Config.get('DEFAULT_DIRECTORY')
        self._last_directory = '..'+self._current_directory
        os.chdir(self._current_directory)
        self._disk = Disk()
        pass

    def send_devicelist(self, client_sock):
        try:
            partition_list = self._disk.list_partitions()
        except Exception as e:
            client_sock.senderr(e)
        else:
            n = len(partition_list)
            client_sock.send(str(n))

            if n >= 0:
                if client_sock.recv() == 'ok':
                    for name in partition_list:
                        client_sock.send(self._disk.device(name))

            else:
                client_sock.send('No device is available now.')
                    
    def send_basic_partitioninfo(self, client_sock):
        try:
            partition_list = self._disk.list_partitions()
        except Exception as e:
            client_sock.senderr(e)
        else:
            n = len(partition_list)
            client_sock.send(str(n))

            if n >= 0:
                if client_sock.recv() == 'ok':
                    for name in partition_list:
                        info = self._disk.partitioninfo(name)
                        client_sock.send(info.name()+':'+info.size()+':'+info.label()+':'+info.mountpoint())
            else:
                client_sock.send('No partition information is available now.')

    def send_filelist(self, client_sock, path):
        try:
            file_list = os.listdir(path)
        except Exception as e:
            client_sock.senderr(e)
        else:
            n = len(file_list)
            client_sock.send(str(n)) #Send file number
            
            if n >= 0:
                if client_sock.recv() == 'ok':
                    for filename in file_list:
                        client_sock.send(filename)
            else:
                client_sock.send('No file available now.')

    def send_currentfilelist(self, client_sock):
        self.send_filelist(client_sock, self._current_directory)

    def cd(self, client_sock, cmd_list):
        try:
            path = cmd_list[1]

            if os.path.isdir(path):
                    path = os.path.abspath(path) 
                    if path[-1] != '/':
                        path = path+'/'
                        
                    self._last_directory = self._current_directory
                    self._current_directory = path
            else:
                raise Exception(path+' is not a right directory.')

        except Exception as e:
            client_sock.senderr(e)

        else:
            client_sock.send('0')
            client_sock.send('successful')            
            
    def send_current_directory(self, client_sock):
        client_sock.send(self._current_directory)

    def send_file(self, client_sock, cmd_list):
        try:
            filepath = cmd_list[1]

            if not os.path.isfile(filepath):
                raise Exception('File path is not right')

            if not os.path.isabs(filepath):
                filepath = self._current_directory + filepath

            f = open(filepath,'rb')
            
            #Add exception handling here
            file_size = os.path.getsize(filepath)

        except Exception as e:
            client_sock.senderr(e)

            #Send the while times
        else:
            client_sock.send(str(int(math.ceil(float(file_size)/float(BUFFER_SIZE)))))

            while True:
                buff = f.read(BUFFER_SIZE)
                if buff == '':
                    break
                client_sock.send(buff)

    def current_directory(self):
        return _current_directory



    

