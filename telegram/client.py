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

files = {"message": "Alert message from client.py", "chat_id": "5393847647", "photo": None}
files = {"message": "Alert message from client.py", "chat_id": "5393847647", "photo": "VA-.jpg"}
resp = requests.post("http://0.0.0.0:2003/", json=files, verify=False)
print(resp.content)




