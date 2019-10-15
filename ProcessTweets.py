import nltk
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
from collections import Counter
from textblob import TextBlob
from bs4 import BeautifulSoup
import matplotlib.cm as cm
from string import punctuation
from string import digits
import urllib.request
import networkx as nx
import pandas as pd
import itertools
import emoji
import math
import time
import json
import sys
import re

nltk.download('punkt')

# Import tweets
tweets = pd.read_csv('https://raw.githubusercontent.com/cpenalozag/twitter_network/master/tweets/statuses.csv')

# Import spanish stop word dictionary
url_sw = 'https://raw.githubusercontent.com/cpenalozag/twitter_network/master/utils/stopwords-es.json'
response_sw = urllib.request.urlopen(url_sw)
data_sw = response_sw.read()

stop_words = set(json.loads(data_sw))

# Import emoji meanings
emoji_translations = pd.read_csv('https://raw.githubusercontent.com/cpenalozag/twitter_network/master/utils/emojis_translated.csv')

# Get spanish meaning of an emoji
def emoji_meaning(emoji):
  meaning = emoji_translations.loc[emoji_translations['emoji'] == emoji]['translation']
  return meaning.values[0] if not meaning.empty else ''

# Transformations to remove digits and punctuation
remove_digits = str.maketrans('', '', digits)
remove_punctuation = str.maketrans('', '', punctuation)

""" Processes text data in tweets

    text: text of tweet
    word_counts: word count dictionary

    returns processed text, length of content, polarity, subjectivity
"""


def process_text(text, word_counts):
    # Remove links
    text = ' '.join(re.sub("(\w+:\/\/\S+)", " ", text).split())

    # Remove file names

    # Remove mentions
    text = ' '.join(re.sub("(@[A-Za-z0-9^\w]+)", " ", text.replace('@ ', '@').replace('# ', '#')).split())

    # Replace hashtags with words
    if text.count('#') > 0:
        text = ' '.join(re.findall('[A-Z][^A-Z]*', text.replace('#', ' ')))

    # Remove HTML tags
    text = BeautifulSoup(text).get_text()

    # Save content length (exluding links and mentions)
    length = len(text)

    # Remove punctuation symbols
    text = ' '.join(re.sub("[\.\,\¡\¿\!\?\:\;\-\=\*\(\)\[\]\"\'\“\_\+\”\%\/\‘\’]", " ", text).split())
    text = text.translate(remove_digits).translate(remove_punctuation)

    # Lower case to avoid case sensitive problems
    text = text.lower()

    # Replace emojis with names
    text = emoji.demojize(text)

    # Add space between emojis and other characters
    ind = -2
    for c in range(text.count(':')):
        ind = text.find(':', ind + 2)
        if c % 2 == 0:
            newLetter = ' :'
        else:
            newLetter = ': '
        text = "".join((text[:ind], newLetter, text[ind + 1:]))

    # Replace emoji names with spanish meaning
    result = []
    parts = text.split(' ')
    for part in parts:
        if part:
            if part[0] == ':':
                em = handle_emoji_tone(part)
                em = emoji_meaning(em)
                if em:
                    result.append(em)
            else:
                if part not in stop_words:
                    if part not in word_counts:
                        word_counts[part] = 1
                    else:
                        word_counts[part] += 1
                result.append(part)

    text = ' '.join(result)

    # Filter using NLTK library append it to a string
    word_tokens = word_tokenize(text)

    result = [w for w in word_tokens if not w in stop_words]

    text = ' '.join(result)

    if len(text) > 12:

        analysis = TextBlob(text)

        try:
            eng = analysis.translate(to='en')
            sentiment = eng.sentiment
            polarity = sentiment.polarity
            subjectivity = sentiment.subjectivity
            time.sleep(.5)
        except:
            polarity = 0.0
            subjectivity = 0.0

    else:
        polarity = 0.0
        subjectivity = 0.0

    return text, length, polarity, subjectivity


tones = ['_light_skin_tone', '_medium-light_skin_tone', '_medium_skin_tone',
         '_medium-dark_skin_tone', '_dark_skin_tone']


# Method that removes the tone from emojis
def handle_emoji_tone(emoji):
    for t in tones:
        if t in emoji:
            tone = t
            return emoji.replace(tone, '')
    return emoji


''' Text analysis '''

# List to hold part of the dataset
text_analysis = []
text_analysis.append(['tweet_id', 'engagement',
                      'effective_length', 'polarity', 'subjectivity'])

# List to store average engagement
avg_eng = []
avg_eng.append(['id', 'average_engagement', 'common_words', 'common_ht_words',
                'common_hts'])

# for n in G.nodes():
for n in list(G.nodes())[-35:]:
    user_id = int(float(n))

    # Total engagement
    eng = 0
    tweet_count = 0

    # Frequent word dictionary
    freq_words = {}

    # Frequent hashtag dictionary
    freq_hashtags = {}

    # Frequent words in hashtags dictionary
    freq_ht_words = {}

    user_tweets = tweets.loc[tweets['id'] == user_id]
    for index, row in user_tweets.iterrows():

        # Add current engagement
        currEng = int(row['favorite_count']) + int(row['retweet_count'])
        eng += currEng
        tweet_count += 1

        # Get hashtags
        ht = row['hashtags'].split(';') if row['hashtags'] != '-' else []

        # Update hashtag count
        for hashtag in ht:
            if hashtag not in freq_ht_words:
                freq_hashtags[hashtag] = 1
            else:
                freq_hashtags[hashtag] += 1

        # Separate hashtags by capitalization
        ht_words = [re.findall('[a-zA-Z][^A-Z]*', w) for w in ht]

        # Create a list with all the words in the hashtags
        hts = []
        for h in ht_words:
            hts = hts + h

        # Remove digits and lower caps for every hashtag word
        hts = [item.translate(remove_digits).lower() for item in hts]

        # Update hashtag word frequencies
        for word in hts:
            if word not in stop_words:
                if word not in freq_ht_words:
                    freq_ht_words[word] = 1
                else:
                    freq_ht_words[word] += 1

        text, length, polarity, subjectivity = process_text(row['text'], freq_words)

        # Update text in  data frame
        text_analysis.append([row['id'], currEng, length, polarity, subjectivity])
        print('Original:', row['text'], '\nProcessed:', text, '\nPolarity, subjectivity:',
              polarity, subjectivity, '\n')

    if tweet_count > 0:
        average_engagement = eng / tweet_count
    else:
        average_engagement = 0
    c_words = Counter(freq_words)
    c_ht_words = Counter(freq_ht_words)
    c_hashtags = Counter(freq_hashtags)
    avg_eng.append([user_id, average_engagement, c_words.most_common(3),
                    c_ht_words.most_common(3), c_hashtags.most_common(3)])


