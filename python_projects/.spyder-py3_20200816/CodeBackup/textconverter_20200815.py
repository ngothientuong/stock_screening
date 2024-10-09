# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 23:22:31 2020

@author: Tuong Ngo
This is text converter class
"""
import os
class textconverter():
    
    def tolist(self, **kwargs) -> list:
        for self.key in kwargs:
            if self.key == "tickers_file":
                self.filename = kwargs[self.key]
                if not os.path.isfile(kwargs[self.key]):
                    raise ValueError("No argument file ",kwargs[self.key]," exists!!" )
                else:
                    with open(kwargs[self.key], 'r') as self.readobj:
                        self.commastr = self.readobj.readline();
                        self.readobj.close()
            elif self.key == "commastr":
                self.commastr = kwargs[self.key]
        # Parse the element, separate by the commas, add to list
        self.mylist = []
        self.commastr = self.commastr.split(',')
        for self.item in self.commastr:
            self.mylist.append(self.item)
        return self.mylist
    
    def listtostr(self, alist, a_delimiter) -> str:
        self.mylist = alist
        self.delimeter = a_delimiter
        self.mystring = self.delimeter.join(self.mylist)
        #for self.item in self.mylist:
        #    self.mystring = self.mystring + ',' + self.item
        return self.mystring
    # Create a file with 'DROP {TB}'
    def createDroptbFile(self, **kwargs):        
        for self.key in kwargs:
            if self.key == "tickers_file":
                self.filename = kwargs[self.key]
                if not os.path.isfile(kwargs[self.key]):
                    raise ValueError("No argument file ",kwargs[self.key]," exists!!" )
                else:
                    with open(kwargs[self.key], 'r') as self.readobj:
                        self.commastr = self.readobj.readline();
                        self.readobj.close()
            elif self.key == "commastr":
                self.commastr = kwargs[self.key]
        # make a file containing table to drop
        self.drop_tb_file =self.filename + "_droptb.txt"
        self.mylist = self.tolist(tickers_file = self.filename)
        with open(self.drop_tb_file, 'w') as writeobj:
            for self.item in self.mylist:
                self.line = "DROP TABLE " + self.doublequoteTicker(self.item)
                writeobj.write(self.line)
                writeobj.write('\n')
            writeobj.close()
    
    # Create a file with 'SELECT * FROM {TB}'
    def querytbRowFile(self, **kwargs):
        for self.key in kwargs:
            if self.key == "tickers_file":
                self.filename = kwargs[self.key]
                if not os.path.isfile(kwargs[self.key]):
                    raise ValueError("No argument file ",kwargs[self.key]," exists!!" )
                else:
                    with open(kwargs[self.key], 'r') as self.readobj:
                        self.commastr = self.readobj.readline();
                        self.readobj.close()
            elif self.key == "commastr":
                self.commastr = kwargs[self.key]
        # make a file containing table to drop
        self.queryRow = self.filename + "_queryRow.txt"
        self.mylist = self.tolist(tickers_file = self.filename)
        with open(self.queryRow, 'w') as writeobj:
            for self.item in self.mylist:
                self.line = 'SELECT * FROM ' + self.doublequoteTicker(self.item)
                writeobj.write(self.line)
                writeobj.write('\n')
            writeobj.close()
    
    def doublequoteTicker(self, mystring):
        self.reservedkeys = ['INT','/']
        self.mystring = mystring
        for self.restricted_key in self.reservedkeys:
            if self.restricted_key in self.mystring:
                self.mystring = '\"' + self.mystring + '\"'
                break
        return self.mystring            
            
        #file_name = r'C:\Users\Owner\3000_tickers.txt'
        #file_name = r'C:\Users\Owner\500_tickers.txt'
        #file_name2 = file_name + '.bak'
        #with open(file_name2, 'w') as writeobj, open(file_name, 'r') as readobj:
        #    line = readobj.readline()
        #    line = line.split(',')
        #    for item in line:
        #        item = '\"' + item + '\"'
        #        mylist.append(item)
        #    
        #    writeobj.close()
        #    readobj.close()
        
        #print(mylist)
    
    