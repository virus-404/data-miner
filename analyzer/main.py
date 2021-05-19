import requests
import pandas as pd
import json
import ast
import csv 
import stylecloud
from itertools import chain
from tools.database import database as db
from tools.logger import logger as lg

log = lg.Logger('Analyzer')

def main():
    database = db.Database.get_database_instance()
    log.log('Database connection stablished')
    texts = get_tweets_text(database)
    log.log('Tweets\' texts are gathered')
    counted_words = get_weighted_texts(texts)
    log.log('Counting words by filter')
    generate_wordcloud(counted_words)

def get_tweets_text(database):
    return [tweet['text'] for tweet in database['social_networks']['twitter'].find()]  # all


def get_weighted_texts(texts):
    word_list = get_filter()    
    word_counter = {}

    with open('files/counted_words.csv', 'w+', newline='') as file:
        fieldnames = ['word', 'counter']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for text in texts: 
            for word in text.split(): 
              if word in word_list and word not in word_counter.keys():
                  word_counter[word] = 1
              elif word in word_counter.keys():
                  word_counter[word] += 1
        
        for key, value in word_counter.items():
            writer.writerow({'word': key, 'counter': value})

def get_filter():
    with open('files/filter_words.json', 'r', encoding='utf-8') as file:
        filter= json.load(file)
        log.log('Filter is available')
        word_list = list(chain.from_iterable(filter.values()))
    
    return word_list
    
    
    


    


def generate_wordcloud(counted_words):
    pass



    '''
    https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/quickstarts/client-libraries-rest-api?tabs=version-3-1&pivots=programming-language-python
    documents = lang_data_shape(res_json)
    language_api_url, sentiment_url, subscription_key = connect_to_azure(data)
    headers = azure_header(subscription_key)
    with_languages = generate_languages(headers, language_api_url, documents)
    json_lines = combine_lang_data(documents, with_languages)
    document_format = add_document_format(json_lines)
    sentiments = sentiment_scores(headers, sentiment_url, document_format)
    week_score = mean_score(sentiments)
    print(week_score)
    week_logic(week_score)
    '''
 


def lang_data_shape(res_json):
    data_only = res_json["data"]
    doc_start = '"documents": {}'.format(data_only)
    str_json = "{" + doc_start + "}"
    dump_doc = json.dumps(str_json)
    doc = json.loads(dump_doc)
    return ast.literal_eval(doc)

def connect_to_azure(data):
    azure_url = "https://week.cognitiveservices.azure.com/"
    language_api_url = "{}text/analytics/v2.1/languages".format(azure_url)
    sentiment_url = "{}text/analytics/v2.1/sentiment".format(azure_url)
    subscription_key = data["azure"]["subscription_key"]
    return language_api_url, sentiment_url, subscription_key

def generate_languages(headers, language_api_url, documents):
    response = requests.post(language_api_url, headers=headers, json=documents)
    return response.json()

def combine_lang_data(documents, with_languages):
    langs = pd.DataFrame(with_languages["documents"])
    lang_iso = [x.get("iso6391Name")
                for d in langs.detectedLanguages if d for x in d]
    data_only = documents["documents"]
    tweet_data = pd.DataFrame(data_only)
    tweet_data.insert(2, "language", lang_iso, True)
    json_lines = tweet_data.to_json(orient="records")
    return json_lines

def add_document_format(json_lines):
    docu_format = '"' + "documents" + '"'
    json_docu_format = "{}:{}".format(docu_format, json_lines)
    docu_align = "{" + json_docu_format + "}"
    jd_align = json.dumps(docu_align)
    jl_align = json.loads(jd_align)
    return ast.literal_eval(jl_align)

def sentiment_scores(headers, sentiment_url, document_format):
    response = requests.post(
        sentiment_url, headers=headers, json=document_format)
    return response.json()

def week_logic(week_score):
    if week_score > 0.75 or week_score == 0.75:
        print("You had a positive week")
    elif week_score > 0.45 or week_score == 0.45:
        print("You had a neutral week")
    else:
        print("You had a negative week, I hope it gets better")

if __name__ == '__main__':
    main()
