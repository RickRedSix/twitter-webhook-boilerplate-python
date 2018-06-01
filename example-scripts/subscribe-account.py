from TwitterAPI import TwitterAPI

import os

CONSUMER_KEY = os.environ.get('CONSUMER_KEY', None)
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET', None)

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', None)
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET', None)

#The environment name for the beta is filled below. Will need changing in future		
ENVNAME = 'accountsub2'
#Insert Webhook ID returned from running create-webhook.py
#WEBHOOK_ID = '1001877412349652992'

twitterAPI = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

r = twitterAPI.request('account_activity/all/:%s/subscriptions' %
                       ENVNAME, None, None, "POST")

print (r.status_code)
       
