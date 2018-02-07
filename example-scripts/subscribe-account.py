from TwitterAPI import TwitterAPI

import os

CONSUMER_KEY = os.environ.get('CONSUMER_KEY', None)
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET', None)

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', None)
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET', None)

#The environment name for the beta is filled below. Will need changing in future		
ENVNAME = 'env-beta'
#Insert Webhook ID returned from running create-webhook.py
WEBHOOK_ID = '{ID HERE}'


twitterAPI = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

r = twitterAPI.request('account_activity/all/:%s/subscriptions' % ENVNAME, {'webhook_id': WEBHOOK_ID})

print r.text
       
