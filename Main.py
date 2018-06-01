#!/usr/bin/env python
from flask import Flask, request, send_from_directory, make_response
from http import HTTPStatus

import Twitter, hashlib, hmac, base64, os, logging, json

CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET', None)
CURRENT_USER_ID = os.environ.get('CURRENT_USER_ID', None)
	     
app = Flask(__name__)	

#generic index route    
@app.route('/')
def default_route():        
    return send_from_directory('www', 'index.html')    		      

#The GET method for webhook should be used for the CRC check
#TODO: add header validation
@app.route("/webhook", methods=["GET"])
def twitterCrcValidation():
    
    crc = request.args['crc_token']
  
    validation = hmac.new(
        key=bytes(CONSUMER_SECRET, 'utf-8'),
        msg=bytes(crc, 'utf-8'),
        digestmod = hashlib.sha256
    )
    digested = base64.b64encode(validation.digest())
    response = {
        'response_token': 'sha256=' + format(str(digested)[2:-1])
    }

    return json.dumps(response)   
        
#The POST method for webhook should be used for all other API events
@app.route("/webhook", methods=["POST"])
def twitterEventReceived():
	  		
    requestJson = request.get_json()

    #dump to console for debugging purposes
    print(json.dumps(requestJson, indent=4, sort_keys=True))
            
    if 'favorite_events' in requestJson.keys():
        #Tweet Favourite Event, process that
        likeObject = requestJson['favorite_events'][0]
        userId = likeObject.get('user', {}).get('id')          
              
        #event is from myself so ignore (Favourite event fires when you send a DM too)   
        if userId == CURRENT_USER_ID:
            return ('', HTTPStatus.OK)
            
        Twitter.processLikeEvent(likeObject)
                          
    elif 'direct_message_events' in requestJson.keys():
        #DM recieved, process that
        eventType = requestJson['direct_message_events'][0].get("type")
        messageObject = requestJson['direct_message_events'][0].get('message_create', {})
        messageSenderId = messageObject.get('sender_id')   
        
        #event type isnt new message so ignore
        if eventType != 'message_create':
            return ('', HTTPStatus.OK)
            
        #message is from myself so ignore (Message create fires when you send a DM too)   
        if messageSenderId == CURRENT_USER_ID:
            return ('', HTTPStatus.OK)
             
        Twitter.processDirectMessageEvent(messageObject)    
                
    else:
        #Event type not supported
        return ('', HTTPStatus.OK)
    
    return ('', HTTPStatus.OK)

                	    
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 65010.
    port = int(os.environ.get('PORT', 65010))
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.run(host='0.0.0.0', port=port, debug=True)
