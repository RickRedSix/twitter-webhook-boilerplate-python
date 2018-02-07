#!/usr/bin/env python
from flask import Flask, request, send_from_directory, make_response

import Twitter, hashlib, hmac, base64, os

CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET', None)
CURRENT_USER_ID = os.environ.get('CURRENT_USER_ID', None)
	     
app = Flask(__name__)	

#generic index route    
@app.route('/')
def default_route():        
    return send_from_directory('www', 'index.html')    		      

#The GET method for webhook should be used for the CRC check
@app.route("/webhook", methods=["GET"])
def twitterCrcValidation():
    
    crc = request.args['crc_token']
    crc = str(crc)   
    
    validation = hmac.new(
        key=CONSUMER_SECRET,
        msg=crc,
        digestmod = hashlib.sha256
    )
    signature = base64.b64encode(validation.digest())
    
    resp = make_response('{"response_token":"sha256='+signature+'"}', 200, {'Content-Type':'application/json'})    
    
    return resp        
        
#The POST method for webhook should be used for all other API events
@app.route("/webhook", methods=["POST"])
def twitterEventReceived():
	  		
    requestJson = request.get_json()               
            
    if 'favorite_events' in requestJson.keys():
        #Tweet Favourite Event, process that
        likeObject = requestJson['favorite_events'][0]
        userId = likeObject.get('user', {}).get('id')          
              
        #event is from myself so ignore (Favourite event fires when you send a DM too)   
        if userId == CURRENT_USER_ID:
            return None   
            
        Twitter.processLikeEvent(likeObject)
                          
    elif 'direct_message_events' in requestJson.keys():
        #DM recieved, process that
        eventType = requestJson['direct_message_events'][0].get("type")
        messageObject = requestJson['direct_message_events'][0].get('message_create', {})
        messageSenderId = messageObject.get('sender_id')   
        
        #event type isnt new message so ignore
        if eventType != 'message_create':
            return None
            
        #message is from myself so ignore (Message create fires when you send a DM too)   
        if messageSenderId == CURRENT_USER_ID:
            return None                
             
        Twitter.processDirectMessageEvent(messageObject)    
                
    else:
        #Event type not supported
        return None
    
    return None

                	    
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 65010.
    port = int(os.environ.get('PORT', 65010))
    app.run(host='0.0.0.0', port=port)