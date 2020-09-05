import json
import tweepy

import engine


with open('keys.json', 'r') as creds:
    keys = json.load(creds)

eng = engine.Engine(keys)