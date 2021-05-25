
import numpy as np
import csv
import random

from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
from palettable.colorbrewer.qualitative import Dark2_8


def create(csvf, font, icon, name, filtered=True): 
    csvf = "files/csvs/"+ csvf
    font = "files/fonts/" + font
    icon = "files/icons/"+ icon
    name = "files/results/"+ name

    words = read_csv(csvf, filtered)
    mask = create_mask(icon)
    build(font, mask, words, name)
    
    # http://stackoverflow.com/questions/7911451/pil-convert-png-or-gif-with-transparency-to-jpg-without

def read_csv(csvf, filtered):
    words_array = {}
    not_wanted = []

    with open ('files/not_wanted_list.txt', 'r') as f: 
        not_wanted = f.read().splitlines()

    with open(csvf, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        if filtered:
            for row in reader:
                words_array[row['word'].upper()] = float(row['counter'])
        else:
            for row in reader:
                if row['word'].startswith('http') or row['word'] in not_wanted:
                    pass
                elif float(row['counter']) < 1000:
                    pass
                else:
                    words_array[row['word'].upper()] = float(row['counter'])
            

    return words_array

def create_mask(icon):
    icon = Image.open(icon)
    mask = Image.new("RGB", icon.size, (255, 255, 255))
    mask.paste(icon, icon)
    return np.array(mask)

def build(font, mask, words, name):
    stopwords = set(STOPWORDS)
    wc = WordCloud(font_path=font, background_color="black", max_words=2000, mask=mask,
                max_font_size=300, random_state=42, scale=2.0, stopwords=stopwords)

    # generate word cloud
    wc.generate_from_frequencies(words)

    #wc.recolor(color_func=ImageColorGenerator(mask))
    wc.recolor(color_func=color_func, random_state=3)
    wc.to_file(name)

def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return tuple(Dark2_8.colors[random.randint(0, 7)])


