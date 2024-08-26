#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 14:16:11 2022

@author: henry

Base on this code: https://benalexkeen.com/send-whatsapp-messages-using-python/


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
        logging.FileHandler('whatsapp_api.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

parser = argparse.ArgumentParser()
parser.add_argument('--template', type=str, default= 'alert_template', help='alert/message to send to hikcentral')
parser.add_argument('--token', type=str, default= 'EAAGbyaWqnx4BAKuI4v73SgU7hcyBM...vea93iga5orxutLlQZD', help='Bot token. To get it, go to https://developers.facebook.com/apps/452765346864926/whatsapp-business/wa-dev-console/')
parser.add_argument('--photo', type=str, default= None, help='path of image or image in base64 (no path)')
parser.add_argument('--object-detected', type=str, default= 'Fire', help='Object detected by neural network')
parser.add_argument('--camera-name', type=str, default= 'Camera 1', help='Camera name')
parser.add_argument('--phone-id', type=str, default= '1006....0312', help='Phone ID of sender message (https://developers.facebook.com/apps/452765346864926/whatsapp-business/wa-dev-console/)')
parser.add_argument('--phone-to', type=str, default= '34612345678', help='Recipient phone')
parser.add_argument('--port', default=2004, type=int, help='port of deployment of the API')
opt, unknown = parser.parse_known_args()
logging.info(opt)


# Initialize flask API
app = Flask(__name__)

# Set variables
template, token, photo, object_detected, camera_name, phone_id, phone_to = opt.template, opt.token, opt.photo, opt.object_detected, opt.camera_name, opt.phone_id, opt.phone_to




def send_message(object_detected, camera_name, phone_to):
    
    headers = {
    "Authorization": f"Bearer {token}",
    'Content-Type': 'application/json'
    }
    
    
    msg_body_params = [
        {
            "type": "text",
            "text": object_detected
        },
        {
            "type": "text",
            "text": camera_name
        }
        ]



    data = {
        'messaging_product': 'whatsapp',
        'to': phone_to,
        'type': 'template',
        'template': {
            'name': template,
            'language': {
                'code': 'en_GB' # Supported languages: https://developers.facebook.com/docs/whatsapp/api/messages/message-templates/#supported-languages-
            },
            'components': [
                {
                    'type': 'body',
                    'parameters': msg_body_params
                }
                    
            ]
        }
    }

    # Just for "hello world" template of whatsapp
#    data = { 'messaging_product': 'whatsapp',
#            'to': '3412345678',
#            'type': 'template',
#            'template': {
#                    'name': 'hello_world',
#                    'language': {
#                            'code': 'en_US'}
#                    }
#            }
    
    
    try:
        url = f"https://graph.facebook.com/v13.0/{phone_id}/messages"
        resp = requests.post(url, headers=headers, data=json.dumps(data))
        
        
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
        send_message(object_detected, camera_name, phone_to)
        return Response(response=json.dumps({"msg":"Alert/message sent correctly"}),status=200)
        
    except Exception as e:
        logging.error(e)
        return Response(response=json.dumps({"msg": "Error! Message received from api: " + str(e)}),status=201)
      

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=opt.port)


