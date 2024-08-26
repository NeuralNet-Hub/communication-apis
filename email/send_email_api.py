#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 13:56:50 2022

@author: henry
"""

# Important note: email and domain should be validated in AWS.




import argparse
import smtplib
from flask import Flask, Response, request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import email.utils
import logging
import sys
import json

#logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('email.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

parser = argparse.ArgumentParser()
parser.add_argument('--sender', type=str, default= 'sender@sender.com', help='sender of alert/message to send by email')
parser.add_argument('--sendername', type=str, default= 'Sender Name', help='sender name of alert/message to send by email')
parser.add_argument('--recipient', type=str, default= 'recipient@recipient.com', help='To address')
parser.add_argument('--subject', type=str, default= 'subject alert', help='subject of alert/message to send by email')
parser.add_argument('--body-text', type=str, default= 'body alert', help='body alert/message to send by email')
parser.add_argument('--username-smtp', type=str, default= 'AKIA...F', help='smtp_username with your Amazon SES SMTP user name')
parser.add_argument('--password-smtp', type=str, default= 'BDPxqnLo/xsX....A9Ze', help='smtp_password with your Amazon SES SMTP password.')
parser.add_argument('--image-alert-path', type=str, default= None, help='In case you wan to attach an image')
parser.add_argument('--host-smtp', type=str, default= 'email-smtp.eu-west-1.amazonaws.com', help='replace zone in email-smtp.zone.amazonaws.com with the Amazon SES SMTP')
parser.add_argument('--port-smtp', type=int, default= 587, help='port of SMTP server usually is 587')
parser.add_argument('--port', default=2001, type=int, help='port of deployment (non related with socket)')

opt, unknown = parser.parse_known_args()
logging.info(opt)



# Replace sender@example.com with your "From" address. 
# This address must be verified.
sender = opt.sender
sendername = opt.sendername

# Replace recipient@example.com with a "To" address. If your account 
# is still in the sandbox, this address must be verified.
recipient  = opt.recipient

# The subject line of the email.
subject = opt.subject

# The email body for recipients with non-HTML email clients.
body_text = (opt.body_text
            )

# The HTML body of the email.
#BODY_HTML = """<html>
#<head></head>
#<body>
#  <h1>Amazon SES SMTP Email Test</h1>
#  <p>This email was sent with Amazon SES using the
#    <a href='https://www.python.org/'>Python</a>
#    <a href='https://docs.python.org/3/library/smtplib.html'>
#    smtplib</a> library.</p>
#</body>
#</html>
#            """


# Replace smtp_username with your Amazon SES SMTP user name.
username_smtp = opt.username_smtp

# Replace smtp_password with your Amazon SES SMTP password.
password_smtp = opt.password_smtp

# (Optional) the name of a configuration set to use for this message.
# If you comment out this line, you also need to remove or comment out
# the "X-SES-CONFIGURATION-SET:" header below.
#CONFIGURATION_SET = "ConfigSet"

# If you're using Amazon SES in an AWS Region other than US West (Oregon), 
# replace email-smtp.us-west-2.amazonaws.com with the Amazon SES SMTP  
# endpoint in the appropriate region.
host_smtp = opt.host_smtp
port_smtp = opt.port_smtp


image_alert_path = opt.image_alert_path

# Initialize flask API
app = Flask(__name__)

def send_mail_from_aws(sender, sendername, recipient, body_text, username_smtp, password_smtp, image_alert_path = None):
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = email.utils.formataddr((sendername, sender))
    msg['To'] = recipient
    # Comment or delete the next line if you are not using a configuration set
    #msg.add_header('X-SES-CONFIGURATION-SET',CONFIGURATION_SET)
    
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(body_text, 'plain')
    #part2 = MIMEText(BODY_HTML, 'html')
    
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    #msg.attach(part2)
    
    # To attach image in case provided
    if image_alert_path is not None:
        fp = open(image_alert_path, 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        
        # Define the image's ID as referenced above
        msgImage.add_header('Content-ID', '<image1>')
        msg.attach(msgImage)

    
    # Try to send the message.
    try:  
        server = smtplib.SMTP(host_smtp, port_smtp)
        server.ehlo()
        server.starttls()
        #stmplib docs recommend calling ehlo() before & after starttls()
        server.ehlo()
        server.login(username_smtp, password_smtp)
        server.sendmail(sender, recipient, msg.as_string())
        server.close()
        logging.info("An email has been sent to " + recipient +"!")

    # Display an error message if something goes wrong.
    except Exception as e:
        logging.error("Error: " + str(e))
        raise ValueError(e)




@app.route('/',methods=["POST"])
def send_request():
    options = vars(opt)
    json_data = request.get_json()
    json_data = json.dumps(json_data) # API receive a dictionary, so I have to do this to convert to string
    json_data = json.loads(json_data) # Convert json to dictionary
    options.update(json_data)
    globals().update(options) # Update default values if are passed thrhoug the request, otherwise, default parameters are used in the request
    
    # Send email of your preference
    try:
        send_mail_from_aws(sender, sendername, recipient, body_text, username_smtp, password_smtp, image_alert_path)
        return Response(response=json.dumps({"msg":"Alert/message sent correctly"}),status=200)
    except Exception as e:
        return Response(response=json.dumps({"msg": "Error! Message received from api: "+str(e)}),status=201)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=opt.port)


    
    

