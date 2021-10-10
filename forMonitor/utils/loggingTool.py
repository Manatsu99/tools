# 2021/10/07
# NG

import inspect
import datetime
from logging import getLogger
from logging import DEBUG, INFO, FileHandler, StreamHandler, Formatter, basicConfig

class loggingTool:
    def __init__(self, isDebug=False, isConsole=True, isFile=False, profile="forTest", startTime=None):
        self.isDebug = isDebug
        self.isConsole = isConsole
        self.isFile = isFile
        self.profile = profile
        self.startTime = startTime
        import inspect
        self.name = str(inspect.stack()[1].filename).rsplit('.')[0]
        self.initialize()

    def i_makeDirs(self):
        import configparser
        config = configparser.ConfigParser()
        config.read(self.profile)
        p_name = config.get('profile_name', 'name')
        c_root = config.get('path', 'root')
        c_logs = config.get('path', 'logs')
        fName = self.startTime.strftime('%Y%m%d%H%M%S')+ p_name + self.name
        self.dirPath = c_root+c_logs+self.startTime.strftime('%Y%m%d%H%M%S')+ p_name+'/'
        import os
        os.makedirs(self.dirPath, exist_ok=True)
        self.fName = fName


    def initialize(self):
        self.logger = getLogger(self.name)
        c = StreamHandler()
        if self.isDebug:
            self.logger.setLevel(DEBUG)
            c.setLevel(DEBUG)
        else:
            self.logger.setLevel(INFO)
            c.setLevel(INFO)
        
        self.i_makeDirs()
        f = FileHandler(self.dirPath+self.name+'.log')
        f.setLevel(DEBUG)
        formatter = Formatter('[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s')
        f.setFormatter(formatter)
        c.setFormatter(formatter)
        self.logger.addHandler(f)
        self.logger.addHandler(c)
        self.i('logs save at: '+self.dirPath)
        self.d("Logger Initialization done.")
        
    

    def d(self, message=""):
        self.logger.debug(self.getStr(message))
        

    def dt(self, message=""):
        self.logger.debug('\t'+self.getStr(message))

    def i(self, message=""):
        self.logger.info(self.getStr(message))
    
    def it(self, message=""):
        self.logger.info('\t'+self.getStr(message))

    def getStr(self, message):
        return str(message)