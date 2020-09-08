import shutil
import tweepy
import argparse
from pprint import pprint


class Engine:

    def parseinit(self):
        showarg = self.parser.add_argument_group('show')
        showarg.add_argument('-u', '--user', nargs='+')
        showarg.add_argument('-t', '--tweets', type=int, default=0)

        mearg = self.parser.add_argument_group('me')
        #mearg.add_argument('-t', '--tweets', type=int, default=0)

    def __init__(self, keys):
        self.keys = dict(keys)

        self.auth = tweepy.OAuthHandler(
            self.keys['apiKey'], self.keys['apiSecret'])
        self.auth.set_access_token(
            self.keys['token'], self.keys['tokenSecret'])

        self.columns = int(shutil.get_terminal_size().columns)

        self.api = tweepy.API(self.auth)

        self.parser = argparse.ArgumentParser()

        self.parseinit()
        

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
                print(f'{user.followers_count} Followers    {user.friends_count} Following\n'.center(
                    self.columns))
                print("\n".join(line.center(self.columns)
                                for line in user.description.split("\n")), '\n\n')

                if numtweets:
                    tweets = self.api.user_timeline(id, count=numtweets)
                    for tweet in tweets:
                        print("\n".join(line.center(self.columns)
                                        for line in tweet.text.split("\n")))
                        print('\n', f"{10*'-'}\n".center(self.columns))

            except Exception as err:
                print(f"Error : {err}".center(self.columns))
            finally:
                print('\n', f"{80*'-'}\n".center(self.columns), end='\n\n\n', sep='')

    @wrap
    def me(self, *args):
        argums = self.parser.parse_args(args)
        
        numts = argums.tweets

        try:
            me = self.api.me()
            print(f'{me.name}'.center(self.columns))
            print(f'(@{me.screen_name})'.center(self.columns), end='\n\n')
            print(f'{me.followers_count} Followers    {me.friends_count} Following\n'.center(
                self.columns))
            print("\n".join(line.center(self.columns)
                            for line in me.description.split("\n")), '\n\n')

            if numts:
                tweets = self.api.user_timeline(me.name ,count=numts)
                for tweet in tweets:
                    print("\n".join(line.center(self.columns)
                                    for line in tweet.text.split("\n")))
                    print('\n', f"{10*'-'}\n".center(self.columns))
                    

        except Exception as err:
            print(f"Error : {err}".center(self.columns))
        finally:
            print('\n', f"{40*'-'}\n".center(self.columns), end='\n\n\n',sep='')

    def handler(self, req, *args):
        self.plex = {
            'show': self.show,
            'me': self.me,
            'exit': self.exit,
            'help': self.parser.print_help
        }
        self.plex.get(req.lower(), self.unknown)(*args)
