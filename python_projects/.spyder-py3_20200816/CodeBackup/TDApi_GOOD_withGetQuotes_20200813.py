# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 11:06:16 2020

@author: Tuong Ngo
"""

import json
import os
import time
import datetime
import urllib.parse
from urllib.parse import urlparse
import urllib3
import uuid
# Need multiprocessing to store multiple tokens in memory
# and to run multiple simultaneous processes.
from multiprocessing import shared_memory
import requests
from splinter import Browser
from selenium import webdriver
from selenium.webdriver.common.by import By
# Import global properties object
from GlobalProperties import GlobalProperties
import re


class TDClient():
    """TD Ameritrade API Client Class
    Implement the token expiration check to grab to authorization token
    from refresh token
    Take config file as an argument to grab credentials of the user as well
    as the cache file name
    Prepare various headers to make different type of requests to site
    """
    

    # Define list of required keys in config file
    required_keys = ["tda_real_username", "tda_real_password" , "tda_real_url", "tda_Consumer_Key", "tda_security_question_oldestnephew" , "tda_security_question_father_born" , "tda_security_question_first_pet", "tda_security_question_meet_spouse", "tda_access_token_file", "tda_refresh_token_file"]
    def __init__(self, **kwargs):
        
        # Source global variables as json dictionary
        self.global_dict = GlobalProperties(global_properties_file = r"C:\Users\Owner\.spyder-py3\Tuong_global_properties.py")
        
        # If global_dict object is empty, raise error
        if not self.global_dict:
            print("WARNING: No content in global_properties file or file does not exists");
            raise KeyError ('Content in global')
            self.close()
            
        # Loop through key arguments and ensure key 'config_file'
        # is included for the account
        self.config_exists = False;
        for self.key in kwargs:
            if self.key == "config_file":
                self.config_exists = True;
                self.config_file = kwargs[self.key]
                #self.config_file = kwargs['config_file']
                

        # Raise error if config key isn't included in the arguments
        # Close the object if no config key is included
        if self.config_exists == False:
            print("WARNING: There is no config file included in argument config_key = ");
            raise KeyError ('No config file included')
            self.close()
        elif not os.path.isfile(self.config_file):
            print("WARNING: No valid full path config file exists");
            raise KeyError ('No valid full path file exists')
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
        #print(str(self.config.items()))
       
       

    # Initiate chrome browser
    def browser(self):    

        # define path to chrome driver
        executable_path = self.global_dict.val('chrome_executable_path')
                
        # Set some default behaviors for our browser
        options = webdriver.ChromeOptions()
        # define chrome options
        for option in self.global_dict.val("chrome_options"):
            options.add_argument(option)
        
        # TDA authorization section
        # create a new browser object, by default it is firefox
        # headless False will show browser
        self.tda_browser = Browser(self.global_dict.val('default_browser'), **executable_path, headless = False, options = options)
        return self.tda_browser
    
    # Initiate chrome browser
    def get_auth_code(self):
        # Create stop signal by creating empty file self.config['tda_stop_flag_file']
        if not os.path.isfile(self.config['tda_stop_flag_file']):
            with open(self.config['tda_stop_flag_file'], 'w') as self.writeobj:
                pass
                self.writeobj.close()

        # AUTHORIZATION CODE REQUEST 
        self.tda_auth_browser = self.browser()
        
        auth_method = 'GET'
        self.auth_url = self.config['tda_real_url']
        self.tda_account_id_code = self.config['tda_Consumer_Key'] + '@AMER.OAUTHAP'
        self.auth_code_payload = {'response_type':'code', 'redirect_uri':self.config['tda_redirect_uri'],'client_id':self.tda_account_id_code}
        # build the url
        self.tda_built_auth_url = requests.Request(auth_method, self.auth_url, params = self.auth_code_payload).prepare()
        #print(self.tda_built_auth_url)
        self.tda_built_auth_url = self.tda_built_auth_url.url
        #print(self.tda_built_auth_url)
        
        # go to our authorization url
        self.tda_auth_browser.visit(self.tda_built_auth_url)
        
        # Fill id element for username
        self.tda_auth_browser.find_by_id("username0").fill(self.config['tda_real_username'])

        # Fill id element for password
        self.tda_auth_browser.find_by_id("password").fill(self.config['tda_real_password'])

        # Click login button
        self.tda_auth_browser.find_by_id("accept").first.click()

        # Click on "Can't get the text message?"" to make "Answer a Security Question" visible
        self.tda_auth_browser.find_by_text("Can't get the text message?").first.click()

        # Click on "Answer a security question" to open security question page
        self.tda_auth_browser.find_by_name("init_secretquestion").first.click()
        
        # Find the Question box to parse the security question
        # Get all the elements available with tag name 'p'
        self.elements = self.tda_auth_browser.find_by_tag('p')
        #for self.key in self.config['tda_security_keys']:
        #    print(self.config['tda_security_keys'][self.key])
        for self.e in self.elements:
        # If the keyword found, return as a non empty list, then anser the box
            for self.key in self.config['tda_security_keys']:
                if re.findall(self.key, self.e.text):
                    self.tda_auth_browser.find_by_id("secretquestion0").fill(self.config['tda_security_keys'][self.key])
        del self.e, self.elements        
        
        time.sleep(0.1)
        # click the continue button
        self.tda_auth_browser.find_by_id("accept").first.click()
        
        # Trust This device screen will show
        # Click on "Yes, trust this device" radio button
        self.elements = self.tda_auth_browser.find_by_tag('label')
        for self.e in self.elements:
            if re.findall(r'Yes,', self.e.text):
                self.e.click()
                break
        del self.e, self.elements
        
        # Click "Save"
        self.tda_auth_browser.find_by_id("accept").first.click()
        
        time.sleep(0.5)
        # Screen asking to for this app to access real TD Ameritrade account will show
        # Click Allow
        self.tda_auth_browser.find_by_id("accept").first.click()
        # give it a sec to load
        time.sleep(1)
        self.tda_new_auth_browser = self.tda_auth_browser.url        
        # grab the url and parse it
        self.new_tda_authorization_code = urllib.parse.unquote(self.tda_new_auth_browser.split("code=")[1])
        
        # Close the browser
        self.tda_auth_browser.quit()
        #print("New authorization code is: " + self.new_tda_authorization_code)
        return self.new_tda_authorization_code
        
    # Obtain access key with authCode
    def useAuthCode_getAccessKey(self):
        self.my_new_tda_authorization_code = self.get_auth_code()
        # define authorization URL with acccess token
        self.tda_authorization_token_url = self.config['tda_authorization_token_url']
        # define the headers
        self.tda_accessToken_request_headers = self.config['tda_accessToken_request_headers']
        # define payload
        self.tda_accessToken_request_payload = {'grant_type':'authorization_code',
                                                'access_type':'offline',
                                                'code':self.my_new_tda_authorization_code,
                                                'redirect_uri':self.config['tda_redirect_uri'],
                                                'client_id':self.config['tda_Consumer_Key']
                                                }
        # print payload
        #print(self.tda_accessToken_request_payload)
        #print(self.tda_accessToken_request_headers)
        #print(self.tda_authorization_token_url)
        # post the data to get token
        self.tda_authReply = requests.post(self.tda_authorization_token_url, headers = self.tda_accessToken_request_headers, data = self.tda_accessToken_request_payload)
        
        if self.tda_authReply.status_code == 200:
            #print(self.tda_authReply)
            
            # convert jason string to dictionary
            self.tda_decoded_auth_content = self.tda_authReply.json()
            #tda_decoded_content
            
            # Record the current epoch time
            # To keep track of refresh_token
            self.refresh_token_time_received = int(time.time());
            
            # Record the current epoch time to keep track of access token
            self.access_token_time_received = int(time.time());
            
            # Add current refresh token time to response json string
            # to keep in the cache file
            self.tda_decoded_auth_content.update({'access_token_received_at':self.access_token_time_received,'refresh_token_received_at':self.refresh_token_time_received})
            
            #print(self.tda_decoded_auth_content)
            
            # dump the json content into the cache file
            with open(self.config['tda_accessToken_cache_file'], 'w') as self.writeobj:
                json.dump(self.tda_decoded_auth_content, self.writeobj)
                self.writeobj.close()
        else:
            print("Status code: ", self.tda_authReply.status_code)
            print("MAJOR ERROR: Could not get access code!!! Check your browser login")
            raise KeyError ('MAJOR ERROR!!!! COULD NOT GET ACCESS CODE VIA BROWSER LOGIN \
                            EXITING NOW!!!')
            self.close()
        
        # Remove the flag that stops other operation to allow normal operation again
        os.remove(self.config['tda_stop_flag_file'])
    
    # Retrieve keys from cache file
    def get_cache(self) -> dict:
        # If stop flag exists or cache file not found retry for 5 seconds
        self.index = 0;
        while self.index < 50:
            if os.path.isfile(self.config['tda_stop_flag_file']) or not os.path.isfile(self.config['tda_accessToken_cache_file']):
                time.sleep(0.1)
                self.index += 1;
                self.iscacheable = False
            else:
                self.iscacheable = True
                break
        if self.iscacheable == False:
            print("WARNING: The file ", self.config['tda_accessToken_cache_file'], " does NOT exists! \
                  OR stop flag file ", self.config['tda_stop_flag_file'], " is present \
                  Please rerun method .useAuthCode_getAccessKey() to authenticate again and produce the file")
            raise KeyError ("The file ", self.config['tda_accessToken_cache_file'], " does NOT exists OR stop flag file ", self.config['tda_stop_flag_file'], " is present" )
            #self.close()
        else:
            with open(self.config['tda_accessToken_cache_file'], 'r') as self.readobj:
                self.tda_cache = json.loads(self.readobj.readline())
                self.readobj.close()
                return self.tda_cache
          
    # Retrieve Refresh Token
    def get_refreshToken(self):
        self.my_TDA_cache = self.get_cache()
        return self.my_TDA_cache['refresh_token']
    
     # Retrieve access Token
    def get_accessToken(self):
        self.my_TDA_cache = self.get_cache()
        return self.my_TDA_cache['access_token']
    
     # Retrieve refresh token received time
    def get_timeReceived_accessToken(self):
        self.my_TDA_cache = self.get_cache()
        return self.my_TDA_cache['access_token_received_at']
    
    # Retrieve refresh token received time
    def get_timeReceived_refreshToken(self):
        self.my_TDA_cache = self.get_cache()
        return self.my_TDA_cache['refresh_token_received_at']
    
    # Retrieve access token expire time
    def accessToken_expires_at(self):
        self.my_TDA_cache = self.get_cache()
        self.access_token_expire = self.my_TDA_cache['access_token_received_at'] + 1800
        return datetime.datetime.fromtimestamp(self.access_token_expire).isoformat()
    
    # Retrieve refresh token expire time
    def refreshToken_expires_at(self):
        self.my_TDA_cache = self.get_cache()
        self.refresh_token_expire = self.my_TDA_cache['refresh_token_received_at'] + 7776000
        return datetime.datetime.fromtimestamp(self.refresh_token_expire).isoformat()
        
    def accessToken_ttl(self):
        self.my_TDA_cache = self.get_cache()
        # if the time to expiration is less than or equal to 0, return 0.
        if int(time.time()) + 60 >= self.my_TDA_cache['access_token_received_at'] + 1800:
            return 0
        else:
            # Update ttl in cache file
            self.myaccessToken_ttl = self.my_TDA_cache['access_token_received_at'] + 1800 - int(time.time())
            self.my_TDA_cache.update({'expires_in':self.myaccessToken_ttl})
            # dump the json content into the cache file
            with open(self.config['tda_accessToken_cache_file'], 'w') as self.writeobj:
                json.dump(self.my_TDA_cache, self.writeobj)
                self.writeobj.close()
            # return time to live of access token otherwise
            return self.my_TDA_cache['access_token_received_at'] + 1800 - int(time.time())
    def refreshToken_ttl(self):
        self.my_TDA_cache = self.get_cache()
        # if the time to expiration is less than or equal to 0, return 0.
        # Note that time.time() will return your current time
        #if time.time() + 60 >= time.time() + int(self.my_TDA_cache['refresh_token_expires_in']):
        if int(time.time()) + 60 >= self.my_TDA_cache['refresh_token_received_at'] + 7776000:
            return 0
        else:
            # Update ttl for refresh_token in cache file
            self.myrefreshToken_ttl = self.my_TDA_cache['refresh_token_received_at'] + 7776000 - int(time.time())
            self.my_TDA_cache.update({'refresh_token_expires_in':self.myrefreshToken_ttl})
            # dump the json content into the cache file
            with open(self.config['tda_accessToken_cache_file'], 'w') as self.writeobj:
                json.dump(self.my_TDA_cache, self.writeobj)
                self.writeobj.close()
            # return time to live of refresh token otherwise
            return self.myrefreshToken_ttl
    
    # Obtain access key with refresh token
    def useRefreshToken_renewAccessKey(self):
        
        # Note that the response does NOT contain refresh token info
        # in this renewal of access token using fresh token        
        # Grab the refresh token
        self.my_tda_refresh_token = self.get_refreshToken()
        # Grab refresh token ttl to reinsert into the response
        self.my_tda_refresh_token_ttl = self.refreshToken_ttl()
        
        # Record the current epoch time
        # To keep track of refresh_token and access token
        self.refresh_token_time_received = self.get_timeReceived_refreshToken()
        self.access_token_time_received = self.get_timeReceived_accessToken()
        
        self.tda_authorization_token_url = self.config['tda_authorization_token_url']
        # define the headers
        self.tda_accessToken_request_headers = self.config['tda_accessToken_request_headers']
        # define payload
        self.tda_accessToken_request_payload = {'grant_type':'refresh_token',
                                                'refresh_token':self.my_tda_refresh_token,
                                                'client_id':self.config['tda_Consumer_Key']
                                                }
        
        # Create stop signal by creating empty file self.config['tda_stop_flag_file']
        if not os.path.isfile(self.config['tda_stop_flag_file']):
            with open(self.config['tda_stop_flag_file'], 'w') as self.writeobj:
                pass
                self.writeobj.close()
                
        # post the data to get token
        self.tda_authReply = requests.post(self.tda_authorization_token_url, headers = self.tda_accessToken_request_headers, data = self.tda_accessToken_request_payload)
        
        if self.tda_authReply.status_code == 200:
            #print(self.tda_authReply)
            
            # convert jason string to dictionary
            self.tda_decoded_auth_content = self.tda_authReply.json()
            
            # Append refresh token and 'refresh token expires in' (ttl) to the 
            # returned URL
            #tda_decoded_content
            self.tda_decoded_auth_content.update({'access_token_received_at':self.access_token_time_received,'refresh_token_received_at':self.refresh_token_time_received,'refresh_token': self.my_tda_refresh_token,'refresh_token_expires_in':self.my_tda_refresh_token_ttl})
            #self.tda_decoded_auth_content = self.tda_decoded_auth_content.update({'refresh_token_expires_in': self.refreshToken_ttl(),'refresh_token': self.my_tda_refresh_token})
                        
            # dump the json content into the cache file
            with open(self.config['tda_accessToken_cache_file'], 'w') as self.writeobj:
                json.dump(self.tda_decoded_auth_content, self.writeobj)
                self.writeobj.close()
            
        else:
            print("Status code: ", self.tda_authReply.status_code)
            print("MAJOR ERROR: Could not get access code!!! Check your browser login")
            raise KeyError ('MAJOR ERROR!!!! COULD NOT GET ACCESS CODE VIA BROWSER LOGIN \
                            EXITING NOW!!!')
            self.close()
        
        # Give it a second for other processes to recognize that there is a stop flag file
        # So those existing process can stop trying to fetch quotes
        # Using old access key
        # Remove the flag that stops other operation to allow normal operation again
        time.sleep(1)
        os.remove(self.config['tda_stop_flag_file'])
        
    
    ## QUOTE request
    def getQuotes(self, symbols):
        # Get valu from cache file
        self.my_TDA_cache = self.get_cache()        
        # To get REAL time, you MUST put in your access key Bearer + Access_key
        # define Authorization header
        self.tda_getQuotes_headers = { 'Authorization': 'Bearer {token}'.format(token = self.my_TDA_cache["access_token"]) }
        # define quotes URL
        self.tda_getQuotes_url = self.config['tda_live_quotes_url']
        # define the headers
        self.tda_getQuotes_request_headers = self.config['tda_liveQuotes_request_headers']
        # define payload
        self.tda_getQuotes_request_payload = {
            
                                                'symbol':symbols,
                                                'apikey':self.config['tda_Consumer_Key']
                                                }

        print('This is params :', self.tda_getQuotes_request_payload)
        self.tda_getQuotesReply = requests.get(self.tda_getQuotes_url, headers = self.tda_getQuotes_headers, params = self.tda_getQuotes_request_payload, verify = True)

        if self.tda_getQuotesReply.status_code == 200:
            #print(self.tda_authReply)
            
            # convert jason string to dictionary
            self.tda_decoded_getQuotes_content = self.tda_getQuotesReply.json()
            # print the quotes
            print(self.tda_decoded_getQuotes_content)
            
            
            # Add current refresh token time to response json string
            # to keep in the cache file
            #self.tda_decoded_auth_content.update({'access_token_received_at':self.access_token_time_received,'refresh_token_received_at':self.refresh_token_time_received})
            
            #print(self.tda_decoded_auth_content)
            
            # dump the json content into the cache file
            #with open(self.config['tda_accessToken_cache_file'], 'w') as self.writeobj:
            #    json.dump(self.tda_decoded_auth_content, self.writeobj)
            #    self.writeobj.close()