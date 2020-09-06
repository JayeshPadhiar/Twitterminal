import tweepy
import argparse
from pprint import pprint


class Engine:

    def __init__(self, keys):
        self.keys = dict(keys)

        self.auth = tweepy.OAuthHandler(
            self.keys['apiKey'], self.keys['apiSecret'])
        self.auth.set_access_token(
            self.keys['token'], self.keys['tokenSecret'])

        self.api = tweepy.API(self.auth)

        self.parser = argparse.ArgumentParser()

    def unknown(self, *args):
        print('Invalid Function')

    def wrap(task):
        def wrapper(*args):
            print(40*'-', end='\n\n')
            task(*args)
            print(40*'-', end='\n\n')
        return wrapper

    @wrap
    def show(self, *ids):
        for id in ids:
            try:
                user = self.api.get_user(id)
                print('Name : ', user.name, end=' ')
                print("\U0001f535" if user.verified == True else '')
                print('ID : ', user.screen_name)
                print('%d Followers\t%d Following' %
                        (user.followers_count, user.friends_count))
            except Exception:
                print('Error')

            finally:
                print()

    @wrap
    def me(self, *args):
        me = self.api.me()
        print('Name : ', me.name)
        print("\U0001f535")

    def handler(self, req, *args):
        self.plex = {
            'show': self.show,
            'me': self.me
        }
        task = self.plex.get(req.lower(), self.unknown)(*args)