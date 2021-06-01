import json
import ast
import csv
import re
import cloud
import sentiment
import chart

from itertools import chain
from tools.database import database as db
from tools.logger import logger as lg

filtered = True  # filtered by filter_words,json: True uses the filter, off doesn't
name = 'counted_words'  # name of the file

log = lg.Logger('Analyzer')
csv_name = ''
picture_name = ''


def main():
    set_name_files()
    database = db.Database.get_database_instance()
    log.log('Database connection stablished')
    '''
    texts = get_tweets_text(database)  
    textids = get_tweets_idtext(database)
    log.log('Tweets\' texts and ids are gathered')
    log.log('Counting words by filter')
    generate_wordcount_csv(texts)
    log.log('Generating Wordcloud')
    build_wordcloud()
    log.log('Wordcloud generated!') #https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/quickstarts/client-libraries-rest-api?tabs=version-3-1&pivots=programming-language-python
    calculate_sentiment_analysis(textids, database)
    '''
    chart.generate(database, log)

            
def set_name_files():
    global csv_name, picture_name

    if filtered:
        csv_name = name + '_csr.csv'
        picture_name = name + '_csr.png'
    else:
        csv_name = name + '_all.csv'
        picture_name = name + '_all.png'

def get_tweets_text(database):
    return [tweet['text'] for tweet in database['social_networks']['twitter'].find()]  # all

def get_tweets_idtext(database):
    return [{'id': tweet['id'],  'text': tweet['text']} for tweet in database['social_networks']['twitter'].find()]  # all

def generate_wordcount_csv(texts):
    # if a word appears +1 times in a text. It is counted as one.
    word_list = get_filter()
    word_counter = {}
    nleather = False  # to delete the top 1 word, in my case is leather

    if nleather:
        global picture_name, csv_name
        picture_name = picture_name.replace('.png', '_nleather.png')
        csv_name = csv_name.replace('.csv', '_nleather.csv')

    with open('files/csvs/' + csv_name, 'w+', newline='') as f:
        fieldnames = ['word', 'counter']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        if filtered:  # in filter_words
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
        else:  # each word
            for text in texts:
                for word in text.split():
                    word = word.lower()
                    # delete all non alpahnumeric charcater. Also deletes emojis
                    word = re.sub('[^A-Za-z0-9]+', '', word)
                    if word in word_counter.keys():
                        word_counter[word] += 1
                    elif not filtered:
                        word_counter[word] = 1

        if nleather:
            del word_counter['leather']

        for key, value in word_counter.items():
            writer.writerow({'word': key, 'counter': value})

def get_filter():
    with open('files/filter_words.json', 'r', encoding='utf-8') as f:
        json_file = json.load(f)
        log.log('Filter is available')
        word_list = list(chain.from_iterable(json_file.values()))

    return word_list

def build_wordcloud():
    icon = 'cow.png'
    font = 'Swansea-q3pd.ttf'
    cloud.create(csv_name, font, icon, picture_name, filtered)

    # https: // github.com/minimaxir/stylistic-word-clouds/blob/master/wordcloud_dataisbeautiful.py https://minimaxir.com/2016/05/wordclouds/

def calculate_sentiment_analysis(textids, database):
    full_tweets = filter_tweets(textids)
    asso_tweets = filter_by_asso(full_tweets)
    full_ids = withdraw_ids(full_tweets)
    log.log('Ids from tweets are already gathered')
    full_metrics = aggregate_metrics(full_ids, database)
    sentiment.calculate(full_metrics, database, log) 
    sentiment.calculate([], database, log) 

def filter_tweets(textids):
    full_tweets = {key: [] for key in get_filter()}

    for textid in textids:
        for word in full_tweets.keys():
            regex = '\\b' + word.replace(' ', '\\b.*\\b') + '\\b'
            if re.search(regex, textid['text']):
                full_tweets[word].append(textid)
    return full_tweets

def filter_by_asso(full_tweets):
    with open('files/association_words.json', 'r') as f:
        log.log('Association words are available')
        json_file = json.load(f)
        wordlist = json_file['association']
        asso_tweets = {key: [] for key in wordlist}

    for key in asso_tweets.keys():
        asso_tweets[key] = full_tweets[key]
        ids = {}

        for key, value in asso_tweets.items():
            ids[key] = withdraw_ids({key: value})

    with open('files/jsons/ids.json', 'w+') as fout:
        json.dump(ids, fout)

    return asso_tweets

def withdraw_ids(full_tweets):
    ids = []
    for list_tweet in full_tweets.values():
        for twt in list_tweet:
            ids.append(twt['id'])
    return list(set(ids))

def aggregate_metrics(tweet_ids, database):
    metric_tweets = []
    retweet = [] 
    tweets = [tweet for tweet in database['social_networks']['twitter'].find({'id': {'$in':tweet_ids}})]

    for tweet in tweets:    
        if 'referenced_tweets' in tweet.keys():
            if tweet['referenced_tweets'][0]['type'] == 'retweeted':
                key = tweet['referenced_tweets'][0]['id']
                value = tweet['public_metrics']
                retweet.append({'id': key, 'public_metrics': value})
            else: 
                metric_tweets.append({
                    'id': tweet['id'],
                    'text': tweet['text'],
                    'public_metrics': tweet['public_metrics'],
                    'lang': tweet['lang']
                })
        elif 'time-stamp' in tweet.keys():
            metric_tweets.append(tweet)
        else: 
            metric_tweets.append({
                'id': tweet['id'],
                'text': tweet['text'],
                'public_metrics': tweet['public_metrics'],
                'lang': tweet['lang']
            })
    
    for i in range(len(retweet)):
        id = retweet[i]
        for metric in metric_tweets:
            if metric['id'] ==  id['id']:
                for key in id['public_metrics'].keys():
                    metric['public_metrics'][key] += id['public_metrics'][key]

    return metric_tweets

if __name__ == '__main__':
    main()
