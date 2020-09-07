import shutil
import tweepy
import argparse
import subprocess
import os
from pprint import pprint

class Engine:

    def __init__(self, keys):
        self.keys = dict(keys)

        self.auth = tweepy.OAuthHandler(
            self.keys['apiKey'], self.keys['apiSecret'])
        self.auth.set_access_token(
            self.keys['token'], self.keys['tokenSecret'])

        self.columns = int(shutil.get_terminal_size().columns)

        self.api = tweepy.API(self.auth)

        self.parser = argparse.ArgumentParser()

        showarg = self.parser.add_argument_group('show')
        showarg.add_argument('-u', '--user', nargs='+')
        showarg.add_argument('-t', '--tweets', type=int, default=0)

    def exit(self, *args):
        exit()

    def unknown(self, *args):
        print('Invalid Function')

    def wrap(task):
        def wrapper(*args):
            columns = int(shutil.get_terminal_size().columns)
            print()
            print(f"{80*'-'}\n\n".center(columns))
            task(*args)
            print(f"{80*'-'}\n\n".center(columns))
        return wrapper

    @wrap
    def show(self, *args):

        data = self.parser.parse_args(args)

        ids = data.user
        numtweets = data.tweets

        for id in ids:
            try:
                user = self.api.get_user(id)
                print(f'{user.name}'.center(self.columns))
                print(f'(@{user.screen_name})'.center(self.columns), end='\n\n')
                print(f'{user.followers_count} Followers    {user.friends_count} Following\n'.center(self.columns))
                print("\n".join(line.center(self.columns)  for line in user.description.split("\n")), '\n\n')

                if numtweets:
                    tweets = self.api.user_timeline(id, count=numtweets)
                    for tweet in tweets:
                        print("\n".join(line.center(self.columns)  for line in tweet.text.split("\n")), end='\n\n')
                        

            except Exception as err:
                    print(f"Error : {err}".center(self.columns))
            finally:
                print('\n', f"{40*'-'}\n".center(self.columns), sep='')

    @wrap
    def me(self, *args):
        me = self.api.me()
        print('Name : ', me.name)
        print("\U0001f535")

    def handler(self, req, *args):
        self.plex = {
            'show': self.show,
            'me': self.me,
            'exit': self.exit
        }
        self.plex.get(req.lower(), self.unknown)(*args)