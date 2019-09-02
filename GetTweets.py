# encoding: utf-8

import tweepy
import json
import glob
import csv
import os

TWEETS_DIR = 'tweets'

# Twitter API credentials
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN_KEY')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

users = []

# authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


def get_user_names():
    for f in glob.glob('twitter-users/*.json'):
        print "loading " + str(f)
        data = json.load(file(f))

        screen_name = data['screen_name']
        users.append(screen_name)


# initialize a list to hold all the Tweets
alltweets = []


def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method



    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=1)

    # save most recent tweets
    alltweets.extend(new_tweets)
    print(new_tweets[0])

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    new_tweets = api.user_timeline(screen_name=screen_name, count=1, max_id=oldest)

    alltweets.extend(new_tweets)


def write_file():
    # Create the directories we need
    if not os.path.exists(TWEETS_DIR):
        os.makedirs(TWEETS_DIR)

    # write the csv
    with open('tweets.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text"])
        # transform the tweepy tweets into a 2D array that will populate the csv
        outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
        writer.writerows(outtweets)

if __name__ == '__main__':
    get_user_names()