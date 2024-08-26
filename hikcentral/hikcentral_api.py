#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 13:56:50 2022

@author: henry
"""



# Socket client example in python

import socket	#for sockets
import sys
import argparse
from flask import Flask, Response, request
import json
import logging

#logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('hikcentral.log'),
        logging.StreamHandler(sys.stdout)
    ]
)


parser = argparse.ArgumentParser()
parser.add_argument('--message', type=str, default= 'intrusion', help='alert/message to send to hikcentral')
parser.add_argument('--ip-url', type=str, default= '192.168.255.14', help='ip of communication with hikcentral')
parser.add_argument('--timeout', default=10, type=int, help='timeout of connection (in seconds)')
parser.add_argument('--port', default=2000, type=int, help='port of deployment (non related with socket)')
opt, unknown = parser.parse_known_args()
logging.info(opt)

# Global variables (received in request)
message, ip_url, timeout = opt.message, opt.ip_url, opt.timeout


# Initialize flask API
app = Flask(__name__)


def send_alert_hik(
    message = 'intrusion', # alert/message to send to hikcentral
    ip_url = '192.168.255.14', # ip of communication with hikcentral
    timeout = 10 # timeout of connection (in seconds)
):


    #create an INET, STREAMing socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        logging.error('Failed to create socket')
        sys.exit()
    	
    logging.info('Socket Created')
    
    # I don't know yet why I need google
    
    host = 'www.google.com'
    port = 15300
    remote_ip = ip_url

    
    #Connect to remote server
    s.settimeout(timeout)
    try:
        s.connect((remote_ip , port))
        logging.info('Socket Connected to ' + host + ' on ip ' + remote_ip)
    except Exception as e:
        logging.error(e)
        raise ValueError(e)

    
    #Send some data to remote server
    message = message+'\r\n\r\n' # it is important to keep \r\n\r\n, I tried without it and it didn't work
    message = message.encode()
    
    for attempt in range(0,3):
        try :
            #Set the whole string
            s.sendall(message)
        except socket.error:
            #Send failed
            logging.error('Send failed')
            sys.exit()



@app.route('/',methods=["POST"])
def send_request():
    options = vars(opt)
    json_data = request.get_json()
    json_data = json.dumps(json_data) # API receive a dictionary, so I have to do this to convert to string
    json_data = json.loads(json_data) # Convert json to dictionary
    options.update(json_data)
    globals().update(options) # Update default values if are passed thrhoug the request, otherwise, default parameters are used in the request

    # Send the alert to Hikcentral
    try:
        send_alert_hik(message, ip_url, timeout)
        return Response(response=json.dumps({"msg":"Alert/message sent correctly"}),status=200)
    except Exception as e:
        logging.error(e)
        return Response(response=json.dumps({"msg": "Error! Message received from api: " + str(e)}),status=201)
      

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=opt.port)