# 2021/10/07
# NG

import datetime
tz = datetime.timezone(datetime.timedelta(hours=9))
startTime = datetime.datetime.now(tz)

import inspect
from logging import getLogger
from logging import DEBUG, INFO, FileHandler, StreamHandler, Formatter, basicConfig

class loggingTool:
    def __init__(self, isDebug=False, isConsole=True, isFile=False, profile="forTest"):
        self.isDebug = isDebug
        self.isConsole = isConsole
        self.isFile = isFile
        self.profile = profile
        import inspect
        self.name = str(inspect.stack()[1].filename).rsplit('.')[0]
        self.initialize()

    def initialize(self):
        self.logger = getLogger(self.name)
        c = StreamHandler()
        if self.isDebug:
            self.logger.setLevel(DEBUG)
            c.setLevel(DEBUG)
        else:
            self.logger.setLevel(INFO)
            c.setLevel(INFO)
        fName = startTime.strftime('%Y%m%d%H%M%S')+ self.profile + self.name
        self.dirPath = "../../../logs/"+self.profile+"_"+startTime.strftime('%Y%m%d%H%M%S')+'/'
        import os
        os.makedirs(self.dirPath, exist_ok=True)
        f = FileHandler(self.dirPath+fName+'.log')
        f.setLevel(DEBUG)
        formatter = Formatter('[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s')
        f.setFormatter(formatter)
        c.setFormatter(formatter)
        self.logger.addHandler(f)
        self.logger.addHandler(c)
        self.i("Logger Initialization done.")
        

    def d(self, message=""):
        self.logger.debug(message)
        pass

    def i(self, message=""):
        self.logger.info(message)
        pass
