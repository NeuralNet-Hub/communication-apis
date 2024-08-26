#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 13:56:50 2022

@author: henry
"""
# If you want to send SMS to any number, you must buy a number in Twilio

import argparse
from twilio.rest import Client
from flask import Flask, Response, request
import logging
import sys
import json

#logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('sms.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

parser = argparse.ArgumentParser()
parser.add_argument('--sender', type=str, default= '+4471234', help='sender of alert/message to send by SMS')
parser.add_argument('--recipient', type=str, default= '+34612345678', help='To phone address')
parser.add_argument('--body-text', type=str, default= 'Alert from NeuralNet', help='body alert/message to send by SMS')
parser.add_argument('--account-sid', type=str, default= '...', help='account_sid (Download from here: https://www.twilio.com/console)')
parser.add_argument('--auth-token', type=str, default= '...', help='auth_token (Download from here: https://www.twilio.com/console)')
parser.add_argument('--message-id', type=str, default= '...', help='Messaging service ID (Download from here: https://console.twilio.com/us1/develop/sms/try-it-out/send-an-sms)')
parser.add_argument('--port', default=2002, type=int, help='port of deployment (non related with socket)')

opt, unknown = parser.parse_known_args()
logging.info(opt)


# Set variables
sender = opt.sender
recipient  = opt.recipient
body_text = opt.body_text
message_id = opt.message_id

# Authentication Download from here: https://www.twilio.com/console
account_sid = opt.account_sid
auth_token = opt.account_sid


# Initialize flask API
app = Flask(__name__)

def send_sms_from_twilio(sender, recipient, body_text, account_sid, auth_token, message_id):
    # Based on this documentation: https://www.twilio.com/docs/sms/tutorials/how-to-send-sms-messages-python#
    
    
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    # If you delete this, it returns error
    account_sid = "..."
    auth_token = "..."
    client = Client(account_sid, auth_token)
    

    
    # Try to send the SMS
    try:  
        message = client.messages \
            .create(
                 messaging_service_sid=message_id,
                 body=body_text,
                 from_=sender,
                 to=recipient
             )
        logging.info("A SMS has been sent to " + recipient +" with this MESSAGE ID: " +str(message.sid)+"!")

    # Display an error message if something goes wrong.
    except Exception as e:
        logging.error("Error: " + str(e))
        raise ValueError(e)




@app.route('/',methods=["POST"])
def send_request():

    # Get options from client
    options = vars(opt)
    json_data = request.get_json()
    json_data = json.dumps(json_data) # API receive a dictionary, so I have to do this to convert to string
    json_data = json.loads(json_data) # Convert json to dictionary
    options.update(json_data)
    
    # Logs
    logging.info("Options updated:")
    logging.info(options)
    
    # Update
    globals().update(options) # Update default values if are passed thrhoug the request, otherwise, default parameters are used in the request
    
    # Send email of your preference
    try:
        send_sms_from_twilio(sender, recipient, body_text, account_sid, auth_token, message_id) 
        return Response(response=json.dumps({"msg":"SMS Alert/message sent correctly"}),status=200)
    except Exception as e:
        return Response(response=json.dumps({"msg": "Error! Message received from api: "+str(e)}),status=201)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=opt.port)


    
    








