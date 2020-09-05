import json
import tweepy

import engine

print(4*'-' , 'Twitterminal', 4*'-', end='\n\n')

with open('keys.json', 'r') as creds:
    keys = json.load(creds)

eng = engine.Engine(keys)