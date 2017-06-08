#!/usr/bin/python2
import subprocess
import config
import os

class PartitionInfo():
    def __init__(self):

        pass

    def device(self):
        return self._device

    def label(self):
        return self._label


    def name(self):
        return self._name

    def size(self):
        return self._size

    def mounted(self):
        return self._mounted

    def mountpoint(self):
        return self._mountpoint

#Disk is a friend class of PartitionInfo
class Disk():
    def __init__(self):
        self._partitioninfo_dict = dict()
        pass

    #Refresh the partioninfo_dict by using lsblk
    def _refresh(self):

        #Empty the PartitionInfo list
        self._partitioninfo_dict.clear()

        self._lsblk_output = subprocess.check_output(['lsblk','--output','NAME,SIZE,MOUNTPOINT,LABEL','--pair']).split('\n')
        
        #Add PartitionInfo to the list
        for line in self._lsblk_output:

            
            if line:

                pair_list = line.split('" ')

                info = PartitionInfo()

                #The lsblk returns values in pair form
                #Keyword = key
                #key is the second item in the pair after the pair is splited with "


                info._name = pair_list[0].split('"')[1]

                info._device = '/dev/'+info._name

                info._size = pair_list[1].split('"')[1]

                info._mountpoint = pair_list[2].split('"')[1]

                if info._mountpoint:
                    info._mounted = True

                else:
                    info._mounted = False

                # print pair_list[3]

                info._label = pair_list[3].split('"')[1]


            

                self._partitioninfo_dict[info._name] = info


    #List all the available partition 
    def list_partitions(self):
        self._refresh()

        name_list = list()
        for key in self._partitioninfo_dict.iterkeys():
            name_list.append(key)

        return name_list

    def is_mounted(self, partition):
        self._refresh()

        if partition in self._partitioninfo_dict:
            return self._partitioninfo_dict[partition].mounted()
        else:
            return None


        pass

    def partitioninfo(self, partition):
        return self._partitioninfo_dict[partition]

    def device(self, partition):
        self._refresh()
        return self._partitioninfo_dict[partition]._device

    def label(self, partition):
        self._refresh()
        return self._partitioninfo_dict[partition]._label

    def partitioninfo_dict(self):
        self._refresh()
        return self._partitioninfo_dict

    def size(self, partition):
        self._refresh()
        return self._partitioninfo_dict[partition]._size


    def mountpoint(self, partition):
        self._refresh()

        if partition in self._partitioninfo_dict:
            return self._partitioninfo_dict[partition]._mountpoint
        else:
            return None

        pass
        

    def mount(self, partition):
        self._refresh()
        info = self._partitioninfo_dict[partition]
        if info._mounted:
            return None

        else:
            if info._label:
                destination = '/mnt/'+info._label

            else:
                destination = '/mnt/'+info._name

            if not os.path.isdir(destination):
                os.mkdir(destination)

            return subprocess.check_output(['mount',info._device, destination])


    def remount(self, partition):
        self._refresh()

        info = self._partitioninfo_dict[partition]
        
        if info._mountpoint:
            subprocess.check_output(['umount',info._device])
            subprocess.check_output(['mount', info._device, info._mountpoint])
            return True

        else:
            return False



    def umount(self,partition):
        self._refresh()

        info = self._partitioninfo_dict[partition]
        if info._mountpoint:
            subprocess.check_output(['umount',info._device])
    
def main():

    disk = Disk()

    print disk.label('sdb1')
    print disk.device('sdb1')
    print disk.mountpoint('sdb1')
    print disk.is_mounted('sdb1')
    print disk.size('sdb1')
    disk.umount('sdb1')

if __name__ == '__main__':
    main()



        

    
