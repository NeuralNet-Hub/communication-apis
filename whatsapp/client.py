#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 14:41:57 2022

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

files = {"object_detected": "your object", "camera_name": "Camera 1"}
resp = requests.post("http://0.0.0.0:2004/", json=files, verify=False)
print(resp.content)




