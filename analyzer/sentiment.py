import demoji
import json
import requests
import re
import copy
import xml.etree.ElementTree as ET

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def calculate(tweets, database, log):
    client = authenticate_client()
    tweets = delete_unrecognized_language(tweets)
    tweets = clean_tweets(tweets)
    with open ('files/jsons/aggregated_tweets.json', 'w+') as fout:
        json.dump(tweets, fout)

    with open('files/jsons/aggregated_tweets.json', 'r') as read_file:
        tweets = json.load(read_file)
    print(len(tweets))
    delete_analized_twt(tweets, database)
    sentiment_analysis(client, tweets, database)

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

def delete_unrecognized_language(tweets):
    accepted_lang = ['zh','zh-hant','nl','en','fr','de','hi','it','ja','ko','no','pt-BR','pt','es','tr']
    res = [tweet for tweet in tweets if tweet.get('lang', 'None') in accepted_lang]
    return res

def clean_tweets(tweets):
    demoji.download_codes()
    pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    for tweet in tweets:
        text = demoji.replace(tweet['text'], "")
        tweet['text'] = pattern.sub('', text)
        
    return tweets

def delete_analized_twt(tweets, database):
    ids = get_intel_id(database)
    del_ids =[ i for i in range(len(tweets)) if tweets[i]['id'] in ids]
    
    for i in del_ids: 
        del tweets[i]

    with open('files/jsons/aggregated_tweets.json', 'w+') as fout:
        json.dump(tweets, fout)
    print(len(tweets))

def get_intel_id(database):
    return [intel['id'] for intel in database['intelligence']['twitter_sentiment_analysis'].find()]  # all

def sentiment_analysis(client, tweets, database):
    for tweet in tweets:
        document = [{'id': tweet['id'], 'language': tweet['lang'], 'text': tweet['text']}]
        result = client.analyze_sentiment(document)
        docs = [doc for doc in result if not doc.is_error]
        for idx, doc in enumerate(docs):
            tweet['opinion'] = doc.sentiment
        database['intelligence']['twitter_sentiment_analysis'].insert_one(tweet)

    
        
    
