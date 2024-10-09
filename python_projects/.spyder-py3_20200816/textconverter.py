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
        return self.mystring
    
    # This will return the path of the file
    def path(self, fullfilename):
        self.filename = fullfilename
        self.rawfilename = self.filename.split('\\')[-1]
        self.filepath = self.filename.replace(self.rawfilename,'')
        return self.filepath
    
    def numoftickers(self, **kwargs):
        self.mylist = self.tolist(**kwargs)
        return len(self.mylist)
    
    # Obtain list of n tickers and direct content into a file
    # Example: txtObj.maketickerfile(tickers_file = r'C:\Users\Owner\Tickers_lists\3000_tickers.txt', new_file = r'C:\Users\Owner\Tickers_lists\tickerlist1.txt', size = 7, group_number = 1)
    def maketickerfile(self, **kwargs):
        # Set default group_number = 1 as default so you don't have to enter group number
        # if it's the first group
        self.group_number = 1;
        for self.key in kwargs:
            if self.key == "tickers_file":
                self.filename = kwargs[self.key]
                if not os.path.isfile(kwargs[self.key]):
                    raise ValueError("No source file ",kwargs[self.key]," exists!!" )
                else:
                    with open(kwargs[self.key], 'r') as self.readobj:
                        self.commastr = self.readobj.readline();
                        self.readobj.close()
            elif self.key == "new_file":
                self.newfile = kwargs[self.key]
            elif self.key == 'size':
                self.size = kwargs[self.key]
            elif self.key == 'group_number':
                self.group_number = kwargs[self.key]
        # Construct the new list file name in the same directory if path is not given
        if '\\' not in self.newfile:
            self.newfile = self.path(self.filename) + self.newfile
        # Parse the content of source file to get to list
        self.mylist = self.tolist(tickers_file = self.filename)
        self.listholder = []
        # Obtain list of interested group, for example, the 4th group of 3 tickers
        self.index = (int(self.group_number) - 1) * int(self.size)
        self.index_limit = self.index + int(self.size)
        while (self.index < self.index_limit and len(self.listholder) < len(self.mylist)):
            self.listholder.append(self.mylist[self.index])
            self.index += 1
        # Join the list to a new string, separate by a comma 
        self.newlistString = ','.join(self.listholder)
        # Write the content of the string to a new file
        with open(self.newfile, 'w') as writeobj:
            writeobj.write(self.newlistString)
            writeobj.close()

            
        
         
    
    # Create a file with 'DROP {TB}' for SQL server syntax
    def createDroptbFileSQLServer(self, **kwargs):        
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
                self.line = "DROP TABLE " + self.convertSQLticker(self.item) + ';'
                writeobj.write(self.line)
                writeobj.write('\n')
            writeobj.close()
    
    # Create a file with 'SELECT * FROM {TB}' for SQL server syntax
    def querytbRowFileSQLServer(self, **kwargs):
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
                self.line = 'SELECT * FROM ' + self.convertSQLticker(self.item) + ';'
                writeobj.write(self.line)
                writeobj.write('\n')
            writeobj.close()
            
   # Create a file with 'DROP {TB}' for MySQL
    def createDroptbFileMySQL(self, **kwargs):        
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
                self.line = "DROP TABLE " + self.convertSQLticker(self.item) + ";"
                writeobj.write(self.line)
                writeobj.write('\n')
            writeobj.close()            
            
    # Rename SQL Server ticker: special words will be added with 11 at the end
    # Ticker with / will have its / converted to 00 for readability
    # Create a file with 'SELECT * FROM {TB}' for SQL server syntax
    def convertSQLticker(self, mystring):
        self.mystring = mystring
        self.reservedkeys = ['INT', 'ASC', 'LONG','FLOAT']
        for self.restricted_key in self.reservedkeys:
            if '/' in self.mystring:
                self.mystring = '00'.join(self.mystring.split('/'))
            elif self.restricted_key in self.mystring:
                self.mystring = self.mystring + '11'
                break
        return self.mystring   
    
    # Obtain ticker name from table name
    def getTickerFromTb(self, mystring):
        self.mystring = mystring
        if '11' in self.mystring:
            self.mystring = self.mystring.split('11')[0]
            return self.mystring
        elif '00' in self.mystring:
            self.mystring = '/'.join(self.mystring.split('00'))
        return self.mystring
    
    def querytbRowFileMySQL(self, **kwargs):
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
                self.line = 'SELECT * FROM ' + self.prefixMySQLtableName(self.item) + ";"
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
    
    def prefixMySQLtableName(self, mystring):
        self.mystring = mystring
        # If table name contains '/', then change it to _
        self.reservedkeys = ['/']
        self.separater = '_'
        for self.restricted_key in self.reservedkeys:
            if self.restricted_key in self.mystring:
                self.mystring = self.separater.join(self.mystring.split('/'))
                break
        self.mystring = 'tb_' + self.mystring
        return self.mystring        

    def getTickerFromMySQLTb(self, mystring):
        self.mystring = mystring
        self.mystring = self.mystring.split('tb_')[-1]
        self.mystring = '/'.join(self.mystring.split('_'))
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
    
    