#test code no use

import json
import tweepy

with open('keys.json') as apis:
    api_keys = json.load(apis)

with open('user.json') as tokens:
    user_token = json.load(tokens)

auth = tweepy.OAuthHandler(
    api_keys['apiKey'], api_keys['apiSecret'])
auth.set_access_token(
    user_token['token'], user_token['tokenSecret'])

try:
    user = auth.get_username()
    print(user)
except Exception as authEx:
    print('Error : ', authEx)
