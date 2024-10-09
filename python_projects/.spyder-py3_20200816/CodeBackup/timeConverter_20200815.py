# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 09:42:12 2020

@author: Tuong Ngo
This object works between time and epoch
"""
import datetime
class timeConverter():
    
    def epochToDatetime(self,epochtime):
        self.mytimestamp = int(epochtime) / 1000
        self.mytimestamp = datetime.datetime.fromtimestamp(self.mytimestamp).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        #print(self.mytimestamp)
        return self.mytimestamp