# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 12:33:53 2020

@author: Tuong Ngo

This script is for Task Scheduler to run against
Check BOTH access token time to live and Refresh token ttl
If refresh token ttl is less than 30d, perform browser login
If access token ttl is less than 10m, get a new access token

This script needs to run every 5m
"""

from TDApi import TDClient

# Create TD client object for Tuong's profile
cron_TuongTDSession = TDClient(config_file = r"C:\Users\Owner\.spyder-py3\Tuong_Config.py")

# Check refresh token ttl, if less than 30d -> Renew
if cron_TuongTDSession.refreshToken_ttl() < 2592000:
    cron_TuongTDSession.useAuthCode_getAccessKey()
else:
    # Check if access token is less then 10m -> Renew using refresh token
    if cron_TuongTDSession.accessToken_ttl() < 600:
        cron_TuongTDSession.useRefreshToken_renewAccessKey()
del cron_TuongTDSession