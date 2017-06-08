class Config():
    
    instance = None

    def __init__(self):
        self.name = 'rasphub.conf'
        self.configmap = dict()
        self._load()
        pass

    @staticmethod
    def config():
        if Config.instance == None:
            Config.instance = Config()

        return Config.instance

    def _load(self):
        configfile = open(self.name, 'r')
        for line in configfile:

            #Delete whitespace
            line = line.strip()

            #Split words
            params = line.split()

            #Find A=B
            for i in range(len(params)):
                if params[i] == '=' and i > 0:
                    self.configmap[params[i-1]] = params[i+1]

    def valueof(self,key):
        return self.configmap[key]
            


def main():
    print Config.config().valueof('mountpoint')

if __name__ == '__main__':
    main()

