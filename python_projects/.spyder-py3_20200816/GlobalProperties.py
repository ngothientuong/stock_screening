# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 19:23:39 2020

@author: Tuong Ngo
"""
import os

class GlobalProperties():
    """
    This class object return list of usuable variable that 
    can be used by all python scripts
    
    """
    def __init__(self, **kwargs):
        # Loop through key arguments and ensure key 'global_properties_file'
        # is included for the account
        self.config_exists = False;
        for key in kwargs:
            if key == "global_properties_file":
                self.config_exists = True;
                self.config_file = kwargs['global_properties_file']
        # Raise error if config key isn't included in the arguments
        # Close the object if no config key is included
        if self.config_exists == False:
            print("WARNING: There is no global_propertise file included in argument global_properties_file = ");
            raise KeyError ('No global properties file included')
            self.close()
        elif not os.path.isfile(self.config_file):
            print("WARNING: No valid full path global properties file exists");
            raise KeyError ('No valid global properties file exists')
            self.close()
                # After config file in included, import its attribute
        #from self.config_file import tda_real_username
        with open(self.config_file, 'r') as self.readobj:
            self.raw_config_dict = {}
            self.raw_string = '';
            for self.line in self.readobj.readlines():
                if "=" in self.line:
                    self.line = self.line.replace('\n',',')
                    self.raw_string = self.raw_string + self.line
            # Close the file
            self.readobj.close();
        # Convert key = value into a dict
        self.config = eval('dict('+self.raw_string+')') 
        #self.config = dict(map(lambda x: x.split('='), self.raw_string.split(', '))) 
        
    def val(self, key):
        return self.config[key]