import json
import tweepy
import shutil

import engine

print(f"{4*'-'} Twitterminal {4*'-'}\n\n".center(shutil.get_terminal_size().columns))

with open('keys.json', 'r') as creds:
    keys = json.load(creds)

eng = engine.Engine(keys)

req = input(':$ ').strip().split()
eng.handler(req[0], *req[1:])
