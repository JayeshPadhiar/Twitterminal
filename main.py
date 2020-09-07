#!/usr/bin/env python3

import json
import tweepy
import shutil

import engine

print(f"\n{4*'-'} Twitterminal {4*'-'}\n\n")

with open('keys.json', 'r') as creds:
    keys = json.load(creds)

eng = engine.Engine(keys)


while True:
    req = input(':$ ').strip().split()
    eng.handler(req[0], *req[1:])