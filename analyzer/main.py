import requests
import pandas as pd
import json
import ast
from tool.database import database as db


def main():
    database = db.Database.get_database_instance()
    '''
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
