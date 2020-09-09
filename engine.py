import shutil
import tweepy
import argparse

from pprint import pprint

class Engine:

    def __init__(self, auth):

        self.columns = int(shutil.get_terminal_size().columns)
        
        #self.auth = tweepy.OAuthHandler(
        #    self.keys['apiKey'], self.keys['apiSecret'])
        #self.auth.set_access_token(
        #    self.keys['token'], self.keys['tokenSecret'])
        
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
                print('\n\n', f'{user.name}'.center(self.columns), sep='')
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

    def handler(self, req, *args):
        self.plex = {
            'show': self.show,
            'me': self.me,
            'exit': self.exit,
            'help': self.parser.print_help
        }

        try:
            self.plex.get(req.lower(), self.unknown)(*args)
        except Exception as exc:
            print("Error : ", exc)
