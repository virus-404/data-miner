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

log = lg.Logger('Analyzer')
csv_name = 'counted_words_csr.csv'
picture_name = 'counted_words_csr.png'
filtered = False

def main():
    database = db.Database.get_database_instance()
    '''
    log.log('Database connection stablished')
    texts = get_tweets_text(database)
    log.log('Tweets\' texts are gathered')
    log.log('Counting words by filter')
    generate_wordcount_csv(texts)
    log.log('Generating Wordcloud')
    generate_wordcloud()
    log.log('Counting verified users')
    verified = count_verified(database)
    log.log('Generating pie')
    generate_pie(verified)
    https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/quickstarts/client-libraries-rest-api?tabs=version-3-1&pivots=programming-language-python
    '''
    client = authenticate_client()
    #sentiment_analysis_example(client)

def get_tweets_text(database):
    return [tweet['text'] for tweet in database['social_networks']['twitter'].find()]  # all

def generate_wordcount_csv(texts):
    word_list = get_filter()    
    word_counter = {}

    with open('files/csvs/'+ csv_name, 'w+', newline='') as file:
        fieldnames = ['word', 'counter']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        if filtered:
            for word in word_list:
                word_counter[word.lower()] = 1
       
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
    with open('files/filter_words.json', 'r', encoding='utf-8') as file:
        filter= json.load(file)
        log.log('Filter is available')
        word_list = list(chain.from_iterable(filter.values()))
    
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

def generate_pie(data):
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


def sentiment_analysis_example(client):

    documents = [
        "I had the best day of my life. I wish you were there with me."]
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




if __name__ == '__main__':
    main()
