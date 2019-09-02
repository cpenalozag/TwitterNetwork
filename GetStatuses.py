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

# authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

users = []


def get_user_names():
    for f in glob.glob('twitter-users/*.json'):
        print "loading " + str(f)
        data = json.load(file(f))

        screen_name = data['screen_name']
        users.append(screen_name)





def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200, tweet_mode='extended')
    print(new_tweets[0])
    # save most recent tweets
    tweet_list.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = tweet_list[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print "getting %s tweets before %s" % (screen_name, oldest)

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest, tweet_mode='extended')

        # save most recent tweets
        tweet_list.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = tweet_list[-1].id - 1

        print "...%s tweets downloaded so far" % (len(tweet_list))




def write_file(tweet_list):
    # Create the directories we need
    if not os.path.exists(TWEETS_DIR):
        os.makedirs(TWEETS_DIR)

    # write the csv
    with open(TWEETS_DIR+'/'+'statuses.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["user id", "created_at", "text","favorite_count", "retweet_count", "phone", "sensitive", "hashtags", "mentions"])
        # transform the tweepy tweets into a 2D array that will populate the csv

        outtweets = [
            [tweet.author.id, tweet.created_at, tweet.full_text.replace('\n', ' ').encode("utf-8"), tweet.favorite_count,
             tweet.retweet_count, tweet.source, tweet.possibly_sensitive, tweet.entities.get("hashtags"), tweet.entities.get("user_mentions")]
                     for tweet in tweet_list if hasattr(tweet, 'possibly_sensitive')]
        writer.writerows(outtweets)


if __name__ == '__main__':

    get_user_names()
    for un in users:
        # initialize a list to hold all the Tweets
        tweet_list = []
        get_all_tweets(un, tweet_list)
        write_file()
