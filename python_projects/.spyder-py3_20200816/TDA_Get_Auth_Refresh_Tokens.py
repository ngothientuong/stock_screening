# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 01:22:32 2020

@author: Owner
"""

# Source:  https://www.youtube.com/watch?v=ApA7EVwSzg0
# Splinter doc: https://splinter.readthedocs.io/en/latest/finding.html
# Selenium list of options: 
#   https://peter.sh/experiments/chromium-command-line-switches/
#   https://chromium.googlesource.com/chromium/src/+/master/chrome/common/chrome_switches.cc


import time
import urllib
import requests
from splinter import Browser
from selenium import webdriver
from selenium.webdriver.common.by import By
from config import tda_real_username, tda_real_password , tda_real_url, tda_Consumer_Key, tda_security_question_oldestnephew , tda_security_question_father_born , tda_security_question_first_pet, tda_security_question_meet_spouse, tda_access_token_file, tda_refresh_token_file 
import re


# define path to chrome driver
executable_path = {'executable_path':r'C:\Users\Owner\python_projects\chromedriver.exe'}

# Set some default behaviors for our browser
options = webdriver.ChromeOptions()

# Make sure the window is maximized
options.add_argument("--start-maximized")

# Make sure that notification are off
options.add_argument("--disable-notifications")

# TDA authorization section
# create a new browser object, by default it is firefox
tda_browser = Browser("chrome", **executable_path, headless = False, options = options)


# define the components of the url
method = 'GET'
url = tda_real_url
tda_account_id_code = tda_Consumer_Key + '@AMER.OAUTHAP'
payload = {'response_type':'code', 'redirect_uri':'http://localhost/test','client_id':tda_account_id_code}

# build the url
tda_built_url = requests.Request(method, url, params = payload).prepare()
tda_built_url = tda_built_url.url

# go to our url
tda_browser.visit(tda_built_url)

# Fill id element for username
tda_browser.find_by_id("username0").fill(tda_real_username)

# Fill id element for password
tda_browser.find_by_id("password").fill(tda_real_password)

# Click login button
tda_browser.find_by_id("accept").first.click()

# Click on "Can't get the text message?"" to make "Answer a Security Question" visible
tda_browser.find_by_text("Can't get the text message?").first.click()

# Click on "Answer a security question" to open security question page
tda_browser.find_by_name("init_secretquestion").first.click()

# Find the Question box to parse the security question
# Get all the elements available with tag name 'p'
elements = tda_browser.find_by_tag('p')
#join_parameter1=','
for e in elements:
    # The below block is also good to spot matched keywords in a string
    #keywords = ['oldest', 'nephew']
    #matched_keywords = set(e.text.split()) & set(keywords)
    #if matched_keywords:
    #    print(e.text)
    
    # If the keyword found, return as a non empty list, then anser the box
    if re.findall(r'oldest nephew', e.text):
        tda_browser.find_by_id("secretquestion0").fill(tda_security_question_oldestnephew)
    elif re.findall(r'father born', e.text):
        tda_browser.find_by_id("secretquestion0").fill(tda_security_question_father_born)
    elif re.findall(r'first pet', e.text):
        tda_browser.find_by_id("secretquestion0").fill(tda_security_question_first_pet)
    elif re.findall(r'spouse', e.text):
        tda_browser.find_by_id("secretquestion0").fill(tda_security_question_meet_spouse)
del e, elements    
time.sleep(1)
# click the continue button
tda_browser.find_by_id("accept").first.click()

# Trust This device screen will show
# Click on "Yes, trust this device" radio button
elements = tda_browser.find_by_tag('label')
for e in elements:
    if re.findall(r'Yes,', e.text):
        e.click()
        break
del e, elements

# Click "Save"
tda_browser.find_by_id("accept").first.click()

time.sleep(1)
# Screen asking to for this app to access real TD Ameritrade account will show
# Click Allow
tda_browser.find_by_id("accept").first.click()

# give it a sec to load
time.sleep(1)
new_tda_url = tda_browser.url

# grab the url and parse it
new_tda_authorization_code = urllib.parse.unquote(new_tda_url.split("code=")[1])

# Close the browser
tda_browser.quit()

new_tda_authorization_code

# define authorization URL with acccess token
tda_authorization_token_url = r'https://api.tdameritrade.com/v1/oauth2/token'

# define the headers
tda_headers = {'Content-Type':'application/x-www-form-urlencoded'}

# Here, the grant_type is the type of tokens with values: authorization_code or refresh_token

tda_payload = {'grant_type':'authorization_code',
               'access_type':'offline',
               'code':new_tda_authorization_code,
               'redirect_uri':'http://localhost/test',
               'client_id':tda_Consumer_Key               
               # Once refresh_token granted, comment out access_type, code, redirect_uri
               # Then fill out refresh_token below
               #'refresh_token':''
               
              }


# post the data to get token
tda_authReply = requests.post(tda_authorization_token_url, headers = tda_headers, data = tda_payload)

# convert json string to dictionary
tda_decoded_content = tda_authReply.json()
#tda_decoded_content


tda_access_token = tda_decoded_content['access_token']
tda_refresh_token = tda_decoded_content['refresh_token']
#print(tda_access_token)

# store tda_access_token and refresh_token in trading_db
with open(tda_access_token_file, 'w') as writeobj1, open(tda_refresh_token_file , 'w') as writeobj2:
    writeobj1.write(tda_access_token)
    writeobj2.write(tda_refresh_token)
    writeobj1.close()
    writeobj2.close()
    
del tda_decoded_content, tda_access_token, tda_authReply, tda_payload, tda_headers, tda_browser, new_tda_authorization_code, new_tda_url
del tda_built_url, tda_account_id_code, method, url, payload, executable_path


