# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 09:42:12 2020

@author: Tuong Ngo
This object works between time and epoch
"""
import datetime
import time
import os
class timeConverter():
    
    def epochToDatetime(self,epochtime):
        self.mytimestamp = int(epochtime) / 1000
        self.mytimestamp = datetime.datetime.fromtimestamp(self.mytimestamp).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        #print(self.mytimestamp)
        return self.mytimestamp
    
    # Below function will return the time stamp of the file in epoch
    def file_epochtime(self, full_path_file):
        if '\\' not in full_path_file:
            raise Exception ("The argument must be file with full path")
        else:
            self.myfile = full_path_file;
            return os.path.getmtime(self.myfile)
    # Below function will return how old the file is in seconds
    def file_age(self, full_path_file):
        self.myfile = full_path_file
        return time.time() - self.file_epochtime(self.myfile)
        