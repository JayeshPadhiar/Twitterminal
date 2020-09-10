#!/usr/bin/env python3
import sys
import json
import tweepy
import shutil
import webbrowser

import engine


def validate(keys):
    keys = dict(keys)

    apiKey = keys.get('apiKey', None)
    apiSecret = keys.get('apiSecret', None)

    token = keys.get('token', None)
    tokenSecret = keys.get('tokenSecret', None)

    if None in [apiKey, apiSecret, token, tokenSecret]:
        raise Exception('Some credentials are missing.\n')

    else:
        print('Credentials fetched. Running OAuth...')
        oauth = tweepy.OAuthHandler(apiKey, apiSecret)
        oauth.set_access_token(token, tokenSecret)

        try:
            uname = oauth.get_username()
            print('Login Successful !\n')
            print(f'Hello {uname}!'.center(shellcol))
            return oauth

        except Exception as authEx:
            raise Exception(f'OAuth Faluire: {authEx}\n')


def login():
    try:
        with open('keys.json') as apicreds:
            keys = dict(json.load(apicreds))

            apiKey = keys.get('apiKey', None)
            apiSecret = keys.get('apiSecret', None)

            if None in [apiKey, apiSecret]:
                raise Exception('API Credentials missing.\n')
    except Exception as filex:
        print('Error : ', filex)
        exit()

    oauth = tweepy.OAuthHandler(apiKey, apiSecret)
    try:
        oauth_url = oauth.get_authorization_url()
        print('Attempting Login : ', oauth_url)
        webbrowser.open(oauth_url)
        code = input('\nAccess code : ')
        access_tokens = oauth.get_access_token(verifier=code)
        oauth.set_access_token(access_tokens[0], access_tokens[1])
        verified = True
        try:
            uname = oauth.get_username()

            print('Login Successful !\n')
            print(f'Hello {uname}!'.center(shellcol))
            user = {
                'apiKey': apiKey,
                'apiSecret': apiSecret,
                'token': access_tokens[0],
                'tokenSecret': access_tokens[1]
            }
            with open('user.json', 'w') as user_creds:
                json.dump(user, user_creds, indent=4)
            return oauth
        except Exception as authEx:
            print(f'Error: {authEx}\n')
    except Exception as authEx:
        print(authEx)
        print('Try again.')
        exit()


if __name__ == '__main__':

    shellcol = shutil.get_terminal_size().columns

    print(f"\n{4*'-'} Twitterminal {4*'-'}\n")

    try:
        with open('user.json', 'r') as usercreds:
            keys = json.load(usercreds)
    except Exception:
        keys = {}

    try:
        oauth = validate(keys)
    except Exception as validateEx:
        print(f'\nError:\n\t{validateEx}')

        print('Attempting new login... \n')
        oauth = login()

    engine = engine.Engine(oauth)

    while True:
        req = input('\n:$ ').strip().split()
        engine.handler(req[0], *req[1:])