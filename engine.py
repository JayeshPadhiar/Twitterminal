import sys
import json
import shutil
import tweepy
import textwrap
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

    def cell(self, tweet):
        for line in tweet:
            wrapped = textwrap.wrap(line, width=80)
            for wrap in wrapped:
                print(wrap.center(self.columns))
        print(f"{10*'-'}\n".center(self.columns))



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
                    statusarr = self.api.user_timeline(
                        id, count=numtweets, tweet_mode='extended')
                    for status in statusarr:
                        # pprint(tweet._json)
                        tweet = status.full_text.split('\n')
                        self.cell(tweet)

            except Exception as err:
                print(f"Error : {err}".center(self.columns))

            finally:
                pass

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
            print(f"{40*'-'}\n".center(self.columns), end='\n')

            if numts:

                statusarr = self.api.user_timeline(
                    me.name, count=numts, tweet_mode='extended')

                for status in statusarr:
                    # pprint(tweet._json)
                    tweet = status.full_text.split('\n')
                    self.cell(tweet)   

        except Exception as err:
            print(f"Error : {err}")
        finally:
            pass
            #print('\n', f"{40*'-'}\n".center(self.columns), end='\n\n\n',sep='')

    def feed(self, *args):
        try:
            argums = self.parser.parse_args(args)
            numts = argums.tweets
        except Exception as parserr:
            print('\nError : ', parserr)

        try:
            statusarr = self.api.home_timeline(
                count=numts, tweet_mode='extended')

            for status in statusarr:
                # pprint(tweet._json)
                print(
                    f'{status.user.name} (@{status.user.screen_name})'.center(self.columns), sep='')
                tweet = status.full_text.split('\n')
                self.cell(tweet)
                
        except Exception as err:
            print(f"Error : {err}")
        finally:
            pass

    def followers(self, *args):

        follower_count = 0
        followers = tweepy.Cursor(self.api.followers)
        try:
            for follower in followers.items():
                print(f"{10*'-'}".center(self.columns))
                print(f'{follower.name} ({follower.screen_name})'.center(self.columns))
                follower_count += 1

            print(f"{10*'-'}".center(self.columns))
            print(f'{follower_count} followers'.center(self.columns))
            print(f"{20*'-'}\n".center(self.columns))

        except Exception as exc:
            print('Error : ', exc)

        

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

    def follow(self, *args):
        users = list(args)

        print(users)

        for user in users:
            try:
                self.api.create_friendship(user)
                print(f'Followed {user}.')
            except Exception as followEx:
                print('Error : ', followEx)

    def unfollow(self, *args):
        users = list(args)

        print(users)

        for user in users:
            try:
                self.api.destroy_friendship(user)
                print(f'Unfollowed {user}.')
            except Exception as followEx:
                print('Error : ', followEx)

    def handler(self, req, *args):
        self.plex = {
            'me': self.me,
            'show': self.show,
            'feed': self.feed,
            'tweet': self.tweet,
            'follow': self.follow,
            'unfollow': self.unfollow,
            'followers': self.followers,
            'logout': self.logout,
            'help': self.parser.print_help,
            'exit': self.exit
        }

        try:
            self.plex.get(req.lower(), self.unknown)(*args)
        except Exception as exc:
            print("Error : ", exc)
