#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Tue Mar  1 10:45:07 2022

@author: Henry
"""




"""
   ____   _   _                  _                       
  / ___| | | (_)   ___   _ __   | |_       _ __    _   _ 
 | |     | | | |  / _ \ | '_ \  | __|     | '_ \  | | | |
 | |___  | | | | |  __/ | | | | | |_   _  | |_) | | |_| |
  \____| |_| |_|  \___| |_| |_|  \__| (_) | .__/   \__, |
                                          |_|      |___/ 
                                          
The following lines of code show how to make requests to the API
"""



import requests


# ====================== Request example ====================== #

files = {'recipient': '+34612345678', # any number
         'body_text':'Hello, this is a test message', # message to be sent
         #'sender': 'just phone numbers that are validaded in twilio',
         #'account-sid': 'check twillio console in case you want to change default',
         #'auth-token': 'check twillio console in case you want to change default',
         #'message-id': 'check twillio console in case you want to change default'
         }
resp = requests.post('http://0.0.0.0:2002/', json=files, verify=False)
print(resp.content)




