import tweepy
import json
import glob
import csv
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')

TWEETS_DIR = 'tweets'
LIMIT = 200

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

if not os.path.exists(TWEETS_DIR):
    os.makedirs(TWEETS_DIR)

# write the csv
with open(TWEETS_DIR + '/' + 'statuses.csv', 'a+') as f:
    writer = csv.writer(f)
    writer.writerow(
        ["id", "tweet_id", "created_at", "text", "favorite_count", "retweet_count", "phone", "sensitive", "hashtags",
         "no_hashtags", "mentions", "no_mentions", "no_urls", "no_media"])


def get_user_names():
    for f in glob.glob('twitter-users/*.json'):
        data = json.load(file(f))

        screen_name = data['screen_name']
        users.append(screen_name)


def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200, tweet_mode='extended')

    recent = []
    recent.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = recent[-1].id - 1

    user_count = 0
    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0 and user_count<LIMIT:

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest, tweet_mode='extended')

        # update user tweets count
        user_count += len(new_tweets)

        # save most recent tweets
        tweet_list.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = tweet_list[-1].id - 1


def write_file():
    # write the csv
    with open(TWEETS_DIR + '/' + 'statuses.csv', 'a+') as f:
        writer = csv.writer(f)

        # transform the tweepy tweets into a 2D array that will populate the csv

        outtweets = [
            [
                tweet.author.id, tweet.id, tweet.created_at, tweet.full_text.encode("utf-8").replace('\n', ' '),
                tweet.favorite_count,
                tweet.retweet_count, tweet.source, tweet.possibly_sensitive,
                ';'.join([ht.get('text').encode('utf-8') for ht in tweet.entities.get('hashtags')])
                if tweet.entities.get('hashtags') else "-",
                len(tweet.entities.get('hashtags')),
                [um.get('id') for um in tweet.entities.get('user_mentions')],
                len(tweet.entities.get('user_mentions')),
                len(tweet.entities.get('urls')) if tweet.entities.get('urls') is not None else 0,
                len(tweet.entities.get('media')) if tweet.entities.get('media') is not None else 0
            ]
            for tweet in tweet_list
            if hasattr(tweet, 'possibly_sensitive') and not tweet.retweeted and 'RT @' not in tweet.full_text]
        writer.writerows(outtweets)


if __name__ == '__main__':

    print "Loading user information"
    get_user_names()

    tweet_count = 0
    for num, un in enumerate(users):
        print "Collecting tweets for user %s of %s: %s" % (num+1, len(users), un)
        # initialize a list to hold all the Tweets
        tweet_list = []
        get_all_tweets(un)
        tweet_count += len(tweet_list)
        print "%s tweets collected so far" % tweet_count
        write_file()
