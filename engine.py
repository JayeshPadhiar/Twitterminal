import sys
import json
import shutil
import tweepy
import argparse

from pprint import pprint


class Engine:

    def __init__(self, auth):

        self.columns = int(shutil.get_terminal_size().columns)

        self.auth = auth
        self.api = tweepy.API(self.auth)

        self.parser = argparse.ArgumentParser()

        self.initparse()

    def exit(self, *args):
        exit()

    def unknown(self, *args):
        print('Invalid Function')

    def initparse(self):
        self.parser.add_argument('-u', '--user', nargs='+')
        self.parser.add_argument('-t', '--tweets', type=int)

    @staticmethod
    def wrap(task):
        def wrapper(*args):
            columns = int(shutil.get_terminal_size().columns)
            print()
            print(f"{80*'-'}".center(columns))
            task(*args)
            print(f"{80*'-'}\n\n".center(columns))
        return wrapper

    def logout(self, *args):

        key = {
            'apiKey': self.auth.consumer_key.decode(),
            'apiSecret': self.auth.consumer_secret.decode()
        }

        try:
            with open('user.json', 'w') as user:
                json.dump(key, user, indent=4)
                print('User Logout Successful !')
                exit()
        except Exception as exc:
            print('Error : ', exc)
            exit()

    def show(self, *args):
        try:
            argums = self.parser.parse_args(args)
            ids = argums.user
            numtweets = argums.tweets
        except SystemExit as parserr:
            print(f"Error : {parserr}")

        for id in ids:
            try:
                user = self.api.get_user(id)
                print('\n', f'{user.name}'.center(self.columns), sep='')
                print(f'(@{user.screen_name})'.center(self.columns), end='\n\n')
                print(f'{user.followers_count} Followers    {user.friends_count} Following\n'.center(
                    self.columns))
                print("\n".join(line.center(self.columns)
                                for line in user.description.split("\n")), '\n')
                print(f"{40*'-'}\n".center(self.columns), end='\n\n')

                if numtweets:
                    tweets = self.api.user_timeline(id, count=numtweets)
                    for tweet in tweets:
                        print("\n".join(line.center(self.columns)
                                        for line in tweet.text.split("\n")))
                        print('\n', f"{10*'-'}\n".center(self.columns))

            except Exception as err:
                print(f"Error : {err}".center(self.columns))

            finally:
                pass
                #print('\n', f"{80*'-'}\n".center(self.columns), end='\n\n\n', sep='')

    def me(self, *args):

        try:
            argums = self.parser.parse_args(args)
            numts = argums.tweets
        except Exception as parserr:
            print('\nError : ', parserr)

        try:
            me = self.api.me()
            print('\n\n', f'{me.name}'.center(self.columns), sep='')
            print(f'(@{me.screen_name})'.center(self.columns), end='\n\n')
            print(f'{me.followers_count} Followers    {me.friends_count} Following\n'.center(
                self.columns))
            print("\n".join(line.center(self.columns)
                            for line in me.description.split("\n")), '\n')
            print(f"{40*'-'}\n".center(self.columns), end='\n\n')

            if numts:
                tweets = self.api.user_timeline(me.name, count=numts)
                for tweet in tweets:
                    print("\n".join(line.center(self.columns)
                                    for line in tweet.text.split("\n")))
                    print('\n', f"{10*'-'}\n".center(self.columns))

        except Exception as err:
            print(f"Error : {err}")
        finally:
            pass
            #print('\n', f"{40*'-'}\n".center(self.columns), end='\n\n\n',sep='')

    def tweet(self, *args):
        tweet = sys.stdin.read()

        print(f"{20*'-'}\n".center(self.columns))
        print("\n".join(line.center(self.columns)
                        for line in tweet.split("\n")))
        print(f"{20*'-'}\n".center(self.columns))

        conf = input('\nTweet? (y/n) : ')

        try:
            if conf.lower() == 'y':
                self.api.update_status(tweet)
                print('Tweeted !')
            else:
                print('Aborting...')
                return
        except Exception as updEx:
            print('Error : ', updEx)

    def handler(self, req, *args):
        self.plex = {
            'me': self.me,
            'show': self.show,
            'tweet': self.tweet,
            'logout': self.logout,
            'help': self.parser.print_help,
            'exit': self.exit
        }

        try:
            self.plex.get(req.lower(), self.unknown)(*args)
        except Exception as exc:
            print("Error : ", exc)
