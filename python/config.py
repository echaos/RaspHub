import sys
DEFAULT_FILE = 'rasphub.conf'
class Config():
    
    instance = None

    def __init__(self):
        self.name = DEFAULT_FILE
        self.configmap = dict()
        self._load()
        pass

    @staticmethod
    def config():
        if Config.instance == None:
            Config.instance = Config()

        return Config.instance

    @staticmethod
    def get(key):
        return Config.config().valueof(key)

    def _load(self):
        try:
            configfile = open(self.name, 'r')
        except IOError as e:
            print str(e)
        except:
            print 'Unexcepted error', sys.exc_info()[0]

        for line in configfile:

            #Ignore empty lines
            if not line:
                continue

            #Ignore comments in the configuration file
            if line[0] == '#':
                continue

            #Delete whitespace
            line = line.strip()

            #Split words
            params = line.split()

            #Find A=B
            for i in range(len(params)):
                if params[i] == '=' and i > 0:
                    self.configmap[params[i-1]] = params[i+1]

    def valueof(self,key):
        if not key in self.configmap.keys():
            raise Exception(key+" is not an entry inside your rasphub.conf file")
        return self.configmap[key]
            

def main():
    print Config.config().valueof('mountpoint')

if __name__ == '__main__':
    main()

