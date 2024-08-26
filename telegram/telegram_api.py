#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 13:56:50 2022

@author: henry
"""



# Socket client example in python

import sys
import argparse
from flask import Flask, Response, request
import requests
import json
import logging
import base64
import io

#logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('telegram_api.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

parser = argparse.ArgumentParser()
parser.add_argument('--message', type=str, default= 'intrusion', help='alert/message to send to hikcentral')
parser.add_argument('--chat-id', type=str, default= '5393847647', help='chat id of telegram. To get it, go to: "https://api.telegram.org/bot{TOKEN}/getUpdates')
parser.add_argument('--token', type=str, default= '5427606778:AAFwEaucUqnVenu2VwUruHSC40dqWyajgpI', help='Bot token. To get it, go to: BotFather (https://core.telegram.org/bots/api)')
parser.add_argument('--photo', type=str, default= None, help='path of image or image in base64 (no path)')
parser.add_argument('--port', default=2003, type=int, help='port of deployment of the API')
opt, unknown = parser.parse_known_args()
logging.info(opt)


# Initialize flask API
app = Flask(__name__)

# Set variables
message, TOKEN, chat_id, photo = opt.message, opt.token, opt.chat_id, opt.photo

def is_base64(s):
    try:
        return base64.b64encode(base64.b64decode(s)).decode() == s
    except Exception:
        return False


def send_message(message):
    
    try:
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}'
        # url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        resp = requests.post(url)
        
        if resp.status_code == 200:
            logging.info(resp.json())
        else:
            logging.error(resp.json())
            raise ValueError(resp.json())
            
    except Exception as e:
        logging.error(e)
        raise ValueError(e)


def send_photo(chat_id, file):
    
    if is_base64(file):
        try:
            photo = io.BytesIO(base64.b64decode(file))
            files = {'photo': photo}
            url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={chat_id}'
            resp = requests.post(url, files = files)
            
            if resp.status_code == 200:
                logging.info(resp.json())
            else:
                logging.error(resp.json())
                raise ValueError(resp.json())
                
        except Exception as e:
            logging.error(e)
            raise ValueError(e)

    else:
        try:
            files = {'photo': open(file, 'rb')}
            url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={chat_id}'
            resp = requests.post(url, files = files)
            logging.info(resp.json())
            
            if resp.status_code == 200:
                logging.info(resp.json())
            else:
                logging.error(resp.json())
                raise ValueError(resp.json())
                
        except Exception as e:
            logging.error(e)
            raise ValueError(e)
            
            


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
        send_message(message)
        if photo is not None:
            send_photo(chat_id, photo)
        return Response(response=json.dumps({"msg":"Alert/message sent correctly"}),status=200)
        
    except Exception as e:
        logging.error(e)
        return Response(response=json.dumps({"msg": "Error! Message received from api: " + str(e)}),status=201)
      

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=opt.port)


