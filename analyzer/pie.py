
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def generate(database, log):
    log.log('Counting verified users')
    verified = count_verified(database)
    intel = get_intel(database)
    log.log('Generating pie')
    generate_pie2(verified)
    generate_opinion_asso(intel)
    generate_opinion_full(intel)

def count_verified(database):
    data = {'Verified': 0, 'Not verified': 0}
    for user in database['social_networks']['twitter_users'].find():
        if user['verified']:
            data['Verified'] += 1
        else:
            data['Not verified'] += 1

    return data

def get_intel(database):
    return [intel for intel in database['intelligence']['twitter_sentiment_analysis'].find()]

def generate_pie2(data):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    explode = (0, 0.1)   # only 'explode' the 2nd slice (i.e. 'Hogs')
    fig, ax = plt.subplots(figsize=(4, 4))
    colors = ('#2aa7f3', '#d3d3d3')
    ax.pie(data.values(), explode=explode, autopct='%1.1f%%',
            colors=colors, shadow=True, startangle=90)
    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.axis('equal')
    ax.legend(labels=data.keys())
    plt.savefig('files/results/verified.png', transparent=False)

def generate_opinion_asso(intel):

    with open('files/jsons/ids.json', 'r') as read_file:
        ids = json.load(read_file)

    opinon = {}
    for key, value in ids.items():
        opinon[key] = classify_list(intel, value, weighted=False)

    labels = opinon.keys()
    pos = []
    neu = []
    neg = []
    mix = []
    width = 0.35

    for i in opinon.values():
        pos.append(i[0]/sum(i)*100)
        neu.append(i[1]/sum(i)*100)
        neg.append(i[2]/sum(i)*100) 
        mix.append(i[3]/sum(i)*100)

    fig, ax = plt.subplots()
    ax.tick_params(axis='x', labelrotation = 45)
    ax.bar(labels, mix, width, color='#afeeee', label='Mixed')
    ax.bar(labels, neu, width, bottom=mix, color='#f0e68c', label='Neutral')
    L = [i+j for i, j in zip(mix, neu)]
    ax.bar(labels, neg, width, bottom=L, color='#ff4500', label='Negative')
    L = [i+j for i, j in zip(L, neg)]
    ax.bar(labels, pos, width,  bottom=L, color='#32cd32', label='Positive')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.legend(loc='upper right', bbox_to_anchor=(1.2, 0.85))

    plt.gcf().subplots_adjust(bottom=0.2)
    plt.savefig('files/results/asso.png',
                transparent=False, bbox_inches='tight')

def generate_opinion_full(intel):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    explode = (0, 0.1, 0, 0)   # only 'explode' the 2nd slice (i.e. 'Hogs')
    fig, ax = plt.subplots(figsize=(4, 4))
    colors = ('#afeeee','#f0e68c','#ff4500','#32cd32')
    data = classify_list(intel,weighted=True)
    ax.pie(data, explode=explode, autopct='%1.1f%%',
           colors=colors, shadow=True, startangle=90)
    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.axis('equal')
    ax.legend(loc='upper right', bbox_to_anchor=(0.25, 1.1), 
            labels=['Mixed', 'Neutral', 'Negative', 'Positive'])
    plt.savefig('files/results/full_w.png', transparent=False)

def classify_list(intel, ids=None, weighted=False):
    calc = [0,0,0,0]
    if ids is not None: 
        for piece in intel:
            if piece['id'] in ids:
                if piece['opinion'] == 'positive':
                    calc[0] += sum_metrics(piece['public_metrics'], weighted)
                elif piece['opinion'] == 'negative':
                    calc[1] += sum_metrics(piece['public_metrics'], weighted)
                elif piece['opinion'] == 'neutral':
                    calc[2] += sum_metrics(piece['public_metrics'], weighted)
                else:
                    calc[3] += sum_metrics(piece['public_metrics'], weighted)
    else:
        for piece in intel: 
            if piece['opinion'] == 'positive':
                calc[0] += sum_metrics(piece['public_metrics'], weighted)
            elif piece['opinion'] == 'negative':
                calc[1] += sum_metrics(piece['public_metrics'], weighted)
            elif piece['opinion'] == 'neutral':
                calc[2] += sum_metrics(piece['public_metrics'], weighted)
            else:
                calc[3] += sum_metrics(piece['public_metrics'], weighted)
    return calc

def sum_metrics(metrics, weighted):
    res = 1
    if not weighted:
        return res
    else:
        res = metrics['retweet_count'] + metrics['like_count'] + \
            metrics['quote_count'] + metrics['reply_count']
        return res
