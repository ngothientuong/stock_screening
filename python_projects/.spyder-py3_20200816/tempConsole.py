# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 18:05:18 2020

@author: Owner
"""

from textconverter import textconverter
from TDApi import TDClient


txtObj = textconverter()
txtObj.createDroptbFileSQLServer(tickers_file = r'C:\Users\Owner\Tickers_lists\500_tickers.txt')
txtObj.querytbRowFileSQLServer(tickers_file = r'C:\Users\Owner\Tickers_lists\500_tickers.txt')

txtObj.createDroptbFileSQLServer(tickers_file = r'C:\Users\Owner\Tickers_lists\deleteme.txt')
txtObj.querytbRowFileSQLServer(tickers_file = r'C:\Users\Owner\Tickers_lists\deleteme.txt')


TD_TuongSession = TDClient(config_file = r"C:\Users\Owner\.spyder-py3\Tuong_Config.py");
#print(TD_TuongSession.refreshToken_ttl())
print(TD_TuongSession.get_bearerHeader())

txtObj.maketickerfile(tickers_file = r'C:\Users\Owner\Tickers_lists\2000_tickers.txt', new_file = r'C:\Users\Owner\Tickers_lists\tickerlist1.txt', size = 7, group_number = 1)
# =============================================================================
# print(txtObj.numoftickers(tickers_file = r'C:\Users\Owner\Tickers_lists\tickerlist1.txt'));
# =============================================================================


txtObj.createDroptbFileSQLServer(tickers_file = r'C:\Users\Owner\Tickers_lists\tickerlist1.txt')
txtObj.querytbRowFileSQLServer(tickers_file = r'C:\Users\Owner\Tickers_lists\tickerlist1.txt')

#TD_TuongSession = TDClient()
#TD_TuongSession = TDClient(config_file = r"C:\Users\Owner\.spyder-py3\Tuong_Config.py", otherarg = "NONE")
#TD_TuongSession.useRefreshToken_renewAccessKey()
#TD_TuongSession.useAuthCode_getAccessKey()
#TD_AnSession = TDClient(config_file = r"C:\Users\Owner\.spyder-py3\An_Config.py", otherarg = "NONE")    
#TD_TuongSession.useAuthCode_getAccessKey();
#print(TD_TuongSession.get_refreshToken())
#print(TD_TuongSession.accessToken_expires_at())
#print(TD_TuongSession.refreshToken_expires_at())
#print(TD_TuongSession.get_accessToken())
#print(TD_TuongSession.accessToken_ttl())
#print(TD_TuongSession.refreshToken_ttl())
#print("Below is new access token and updated ttl")
#print()
#print()
#TD_TuongSession.useRefreshToken_renewAccessKey()
#print(TD_TuongSession.get_refreshToken())
#print(TD_TuongSession.accessToken_expires_at())
#print(TD_TuongSession.refreshToken_expires_at())
#print(TD_TuongSession.get_accessToken())
#print(TD_TuongSession.accessToken_ttl())
#print(TD_TuongSession.refreshToken_ttl())












