import requests
import json
import ast
import cloud
import csv
import re
import pandas as pd
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from itertools import chain
from tools.database import database as db
from tools.logger import logger as lg

filtered = False #filtered by filter_words,json: True uses the filter, off doesn't
name = 'counted_words' #name of the file

log = lg.Logger('Analyzer')
csv_name = ''
picture_name = ''

def main():
    global csv_name, picture_name

    if filtered:
        csv_name = name + '_csr.csv'
        picture_name = name + '_csr.png'
    else:
        csv_name = name + '_all.csv'
        picture_name = name + '_all.png'

    database = db.Database.get_database_instance()
    log.log('Database connection stablished')
    texts = get_tweets_text(database)
    textids = get_tweets_idtext(database)
    log.log('Tweets\' texts and ids are gathered')
    log.log('Counting words by filter')
    generate_wordcount_csv(texts)
    log.log('Generating Wordcloud')
    generate_wordcloud()
    log.log('Wordcloud generated!')
    '''
    log.log('Counting verified users')
    verified = count_verified(database)
    log.log('Generating pie')
    generate_pie_2opt(verified)
    https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/quickstarts/client-libraries-rest-api?tabs=version-3-1&pivots=programming-language-python
    '''
    client = authenticate_client()
    calculate_sentiment_analysis(client, textids)

def get_tweets_text(database):
    return [tweet['text'] for tweet in database['social_networks']['twitter'].find()]  # all

def get_tweets_idtext(database):
    return [{'id': tweet['id'],  'text': tweet['text']} for tweet in database['social_networks']['twitter'].find()]  # all

def generate_wordcount_csv(texts):
    word_list = get_filter()  
    word_counter = {}

    with open('files/csvs/'+ csv_name, 'w+', newline='') as f:
        fieldnames = ['word', 'counter']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        if filtered: #in filter_words
            for word in word_list:
                word = word.lower()
                word_counter[word] = 1
            
            for text in texts:
                text = text.replace('@', ' ').replace('#', ' ')
                for word in word_list:
                    word = word.lower()
                    regex = '\\b' + word.replace(' ', '\\b.*\\b') + '\\b'
                    if re.search(regex, text):
                        word_counter[word.lower()] += 1
        else: #each word
            for text in texts:
                for word in text.split(): 
                    word = word.lower()
                    word = re.sub('[^A-Za-z0-9]+', '', word)
                    if word in word_counter.keys():
                        word_counter[word] += 1
                    elif not filtered:
                        word_counter[word] = 1

        for key, value in word_counter.items():
            writer.writerow({'word': key, 'counter': value})

def get_filter():
    with open('files/filter_words.json', 'r', encoding='utf-8') as f:
        json_file = json.load(f)
        log.log('Filter is available')
        word_list = list(chain.from_iterable(json_file.values()))
    
    return word_list
       
def generate_wordcloud():
    icon = 'cow.png'
    font = 'Swansea-q3pd.ttf'
    cloud.create(csv_name, font, icon, picture_name, filtered)

    #https: // github.com/minimaxir/stylistic-word-clouds/blob/master/wordcloud_dataisbeautiful.py https://minimaxir.com/2016/05/wordclouds/

def count_verified(database): 
    data = {'Verified': 0, 'Not verified': 0}
    for user in database['social_networks']['twitter_users'].find():
        if user['verified']:
            data['Verified'] += 1
        else: 
            data['Not verified'] += 1

    return data

def generate_pie_2opt(data):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    explode = (0, 0.1)   # only 'explode' the 2nd slice (i.e. 'Hogs')
    fig1, ax1 = plt.subplots(figsize=(4, 4))
    colors = ('#2aa7f3','#d3d3d3')
    ax1.pie(data.values(), explode=explode, labels=data.keys(), autopct='%1.1f%%',
            colors=colors, shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig('files/results/verified.png', transparent=True)

def authenticate_client():
    keys = ET.parse('files/keys.xml')
    tree = keys.getroot()
    key = tree.find('key').text
    endpoint = tree.find('endpoint').text

    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=ta_credential)
    return text_analytics_client

def calculate_sentiment_analysis(client, textids):
    tweets = filter_tweets(textids)
    for tweet in tweets.keys():
        print(tweet,len(tweets[tweet]))


def filter_tweets(textids):
    tweets = {}

    with open ('files/association_words.json', 'r') as f:
        log.log('Association words are available')
        json_file = json.load(f)
        wordlist = json_file['association']
        for word in wordlist:
            tweets[word] = []
    
    for textid in textids:
        for word in wordlist: 
            regex = '\\b' + word.replace(' ', '\\b.*\\b') + '\\b'
            if re.search(regex, textid['text']):
                tweets[word].append(textid)

    return tweets

    
    """
    response = client.analyze_sentiment(documents=documents)[0]
    print("Document Sentiment: {}".format(response.sentiment))
    print("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
        response.confidence_scores.positive,
        response.confidence_scores.neutral,
        response.confidence_scores.negative,
    ))
    for idx, sentence in enumerate(response.sentences):
        print("Sentence: {}".format(sentence.text))
        print("Sentence {} sentiment: {}".format(idx+1, sentence.sentiment))
        print("Sentence score:\nPositive={0:.2f}\nNeutral={1:.2f}\nNegative={2:.2f}\n".format(
            sentence.confidence_scores.positive,
            sentence.confidence_scores.neutral,
            sentence.confidence_scores.negative,
        ))
    """



if __name__ == '__main__':
    main()
