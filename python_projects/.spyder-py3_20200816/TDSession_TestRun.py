# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 15:17:27 2020

@author: Owner
"""
#from multiprocessing import Pool
from TDApi import TDClient
import time
import sys

#from multiprocessing import Pool
#import multiprocessing as mul
#################


#del TD_TuongSession  
if __name__ == '__main__':
    #freeze_support()
    #mytickers_file = r'C:\Users\Owner\Tickers_lists\deleteme.txt'
    #An_mytickers_file = r'C:\Users\Owner\Tickers_lists\500_tickers.txt'
    mytickers_file = sys.argv[1]
    myconfig_file = sys.argv[2]
    TD_TuongSession = TDClient(config_file = r"C:\Users\Owner\.spyder-py3\Tuong_Config.py", otherarg = "NONE")
    TD_TuongSession = TDClient(config_file = myconfig_file)
    #TD_AnSession = TDClient(config_file = r"C:\Users\Owner\.spyder-py3\An_Config.py", otherarg = "NONE")        
    TD_TuongSession.dbCreateMultb(tickers_file = mytickers_file)
    #TD_AnSession.dbCreateMultb(tickers_file = An_mytickers_file)
    initialRuntime = time.time()    
    index = 0
    while (index < 119 and time.time() - initialRuntime < 60):
    #while index < 5:
        starttime = time.time()
        Tuong_large_quote = TD_TuongSession.getQuotes(tickers_file = mytickers_file)
        #An_large_quote = TD_AnSession.getQuotes(tickers_file = An_mytickers_file)
        TD_TuongSession.dbInsertMultiple(Tuong_large_quote) 
        print("That took {} seconds".format(time.time() - starttime))
        index += 1
        print("Finish round ", index)
        print()
        print()
        time.sleep(.4)
    print()    
    print()    
    print("Initial run time is: ", initialRuntime)
    print("Final_runtime is: ",  time.time())
    print("That took {} seconds".format(time.time() - initialRuntime))
    del TD_TuongSession




