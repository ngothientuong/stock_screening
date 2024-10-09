# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 15:17:27 2020

@author: Owner
"""

from TDApi import TDClient

#################

#TD_TuongSession = TDClient()
TD_TuongSession = TDClient(config_file = r"C:\Users\Owner\.spyder-py3\Tuong_Config.py", otherarg = "NONE")
    
TD_TuongSession.useAuthCode_getAccessKey();
print(TD_TuongSession.get_refreshToken())
print(TD_TuongSession.accessToken_expires_at())
print(TD_TuongSession.refreshToken_expires_at())
print(TD_TuongSession.get_accessToken())
print(TD_TuongSession.accessToken_ttl())
print(TD_TuongSession.refreshToken_ttl())
print("Below is new access token and updated ttl")
print()
print()
TD_TuongSession.useRefreshToken_renewAccessKey()
print(TD_TuongSession.get_refreshToken())
print(TD_TuongSession.accessToken_expires_at())
print(TD_TuongSession.refreshToken_expires_at())
print(TD_TuongSession.get_accessToken())
print(TD_TuongSession.accessToken_ttl())
print(TD_TuongSession.refreshToken_ttl())

#del TD_TuongSession  








