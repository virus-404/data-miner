
import pandas as pd
import matplotlib.pyplot as plt

def generate(database, log):
    log.log('Counting verified users')
    verified = count_verified(database)
    log.log('Generating pie')
    generate_pie_2opt(verified)


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
    colors = ('#2aa7f3', '#d3d3d3')
    ax1.pie(data.values(), explode=explode, labels=data.keys(), autopct='%1.1f%%',
            colors=colors, shadow=True, startangle=90)
    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.axis('equal')
    plt.savefig('files/results/verified.png', transparent=True)
