from flask import Flask, request, jsonify
from nltk.tokenize import word_tokenize
from sklearn.externals import joblib
from sklearn import preprocessing
import matplotlib.pyplot as plt
from string import punctuation
from textblob import TextBlob
from bs4 import BeautifulSoup
from flask_cors import CORS
from string import digits
import urllib.request
import pandas as pd
import numpy as np
import matplotlib
import emoji
import numpy
import json
import re

app = Flask(__name__)
CORS(app)


# Helper functions
# Get spanish meaning of an emoji
def emoji_meaning(emoji):
    meaning = emoji_translations.loc[emoji_translations['emoji'] == emoji]['translation']
    return meaning.values[0] if not meaning.empty else ''


def find_urls(text):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    return urls


# Processes text data in tweets
def process_text(text):
    mentions = text.count('@')
    hashtags = text.count('#')
    urls = len(find_urls(text))

    # Remove links
    text = ' '.join(re.sub("(\w+:\/\/\S+)", " ", text).split())

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
                result.append(part)

    text = ' '.join(result)

    # Filter using NLTK library append it to a string
    word_tokens = word_tokenize(text)
    result = [w for w in word_tokens if not w in stop_words]
    text = ' '.join(result)

    # Check if text contains at least a word
    analysis = TextBlob(text)
    try:
        # Sentiment analysis
        eng = analysis.translate(to='en')
        sentiment = eng.sentiment
        polarity = sentiment.polarity
        subjectivity = sentiment.subjectivity

    except Exception as e:
        polarity = 0.0
        subjectivity = 0.0

    result = {
        'no_hashtags': [hashtags],
        'no_mentions': [mentions],
        'no_urls': [urls],
        'effective_length': [length],
        'polarity': [polarity],
        'subjectivity': [subjectivity]
    }

    return result


tones = ['_light_skin_tone', '_medium-light_skin_tone', '_medium_skin_tone',
         '_medium-dark_skin_tone', '_dark_skin_tone']

times = ['afternoon','early morning','late night','morning','night','noon']


# Method that removes the tone from emojis
def handle_emoji_tone(emoji):
    for t in tones:
        if t in emoji:
            tone = t
            return emoji.replace(tone, '')
    return emoji


def preprocess(data):
    # Remove useless columns
    dataset = data.drop(['common_hts', 'screen_name', 'description'], axis=1)

    # Convert boolean data to numbers
    dataset[["sensitive", "verified"]] *= 1

    # One hot encoding for user type
    one_hot2 = pd.get_dummies(dataset['tipo'])
    dataset = dataset.drop('tipo', axis=1)
    dataset = dataset.join(one_hot2)

    # One hot encoding for core
    one_hot3 = pd.get_dummies(dataset['partition'])
    dataset = dataset.drop('partition', axis=1)
    dataset = dataset.join(one_hot3)

    # Set type for categorical variables
    bool_vars = ['sensitive', 'verified']
    time_vars = ['afternoon', 'early morning', 'late night', 'morning', 'night', 'noon']
    type_vars = ['company', 'competition', 'education', 'entertainment', 'event', 'fans', 'gossip', 'government entity',
                 'informative', 'journalism', 'news', 'ngo', 'personal', 'politics', 'radio', 'religion', 'sports']
    cat_vars = bool_vars
    cat_vars.extend(time_vars)
    cat_vars.extend(type_vars)

    dataset[cat_vars] = dataset[cat_vars].astype('category')

    # Transform attributes to [0,1]

    attributes = ['core', 'no_hashtags', 'no_mentions', 'average_engagement', 'listed', 'no_urls', 'effective_length',
                  'no_media', 'polarity', 'in_degree', 'clustering', 'closeness', 'betweenness', 'vote_rank',
                  'authority', 'hubs', 'pagerank']
    dataset[attributes] = scaler.fit_transform(dataset[attributes])

    # Transformation for special variables: followers and friends (keep meaning)
    dataset[['followers', 'friends']] = dataset[['followers', 'friends']].astype(np.int32)
    dataset['followers'] = data['followers'] / 19000000
    dataset['friends'] = data['friends'] / 180000
    dataset = dataset[columns]
    return dataset

@app.route('/predict', methods=['POST'])
def predict():
    req = request.json
    text = req['text']
    media = req['media']
    time = req['time']

    # Process text
    result = process_text(text)

    for t in times:
        if t == time:
            result[t] = [1]
        else:
            result[t] = [0]

    result['sensitive'] = [0]
    result['no_media'] = [media]

    tweet_data = pd.DataFrame(result)
    tweet_data['join'] = 0
    data = user_info.merge(tweet_data, left_index=False, right_index=False)
    dataset = preprocess(data)
    result_list = []

    for index, row in dataset.iterrows():
        entry = list(row)[1:]
        entry = numpy.reshape(entry, (1, -1))
        result_list.append((row['id'], model.predict(entry)[0]))

    result_list.sort(key=lambda tup: tup[1], reverse=True)
    return jsonify({'results': result_list[:20]})


if __name__ == '__main__':
    print('Loading files...')
    # Load model
    model = joblib.load('files/model.pkl')

    # Load scaler
    scaler = joblib.load('files/scaler.pkl')

    # Load columns
    columns = joblib.load('files/model_columns.pkl')

    # Import spanish stop word dictionary
    url_sw = 'https://raw.githubusercontent.com/cpenalozag/twitter_network/master/utils/stopwords-es.json'
    response_sw = urllib.request.urlopen(url_sw)
    data_sw = response_sw.read()

    stop_words = set(json.loads(data_sw))

    # Import emoji meanings
    emoji_translations = pd.read_csv(
        'https://raw.githubusercontent.com/cpenalozag/twitter_network/master/utils/emojis_translated.csv')

    # Transformations to remove digits and punctuation
    remove_digits = str.maketrans('', '', digits)
    remove_punctuation = str.maketrans('', '', punctuation)

    # Load user info
    user_info = pd.read_csv(
        'https://raw.githubusercontent.com/cpenalozag/twitter_network/master/network-data/user_info.csv')
    user_info['join'] = 0

    print('Starting server...')
    app.run(port=8080)
