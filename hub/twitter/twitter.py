import os
import time
import traceback
import xml.etree.ElementTree as ET
import multiprocessing as mp

from tools.logger import logger
from .tweet.filtered_stream import FilteredStream 
from .tweet.update_tweet import UpdateTweet

'''
    Beacuse the API is not giving the mterics of the tweets. The hub needs first the filtered tweet, and then gather the organic metrics.
        -   streaming:  getting filtered streams accordding to the filtered keywords of the folder file.
        -   updating:   getting tweets metrics by sending id.
    It needs to be used first in streaming mode and then in updating mode. 
'''

def set_up():
    cwd = os.getcwd()  # Get the current working directory (cwd)
    os.chdir(cwd + '/twitter')  # Settig the root directory for the file
    return logger.Logger('Twitter') # Setting up the logger
    
def run():
    log = set_up()
    log.log('Twitter setting up')
    tree = ET.parse('files/keys.xml')
    keyring = tree.getroot()
    log.log('Reading credentials')

    mp.set_start_method('fork')
    p = mp.Process(target=streaming_connection, args=(
        keyring.find('bearer-token').text, log,))
    p.start()

    q = mp.Process(target=updating_connection, args=(
        keyring.find('bearer-token').text, log,))
    
    q.start()
    p.join() 
    q.join()

    '''
    mode = 'updating' 
    if mode == 'streaming':
        streaming_connection(keyring.find('bearer-token').text, log)
    else: 
        updating_connection(keyring.find('bearer-token').text, log)
    ''' 

def streaming_connection(token, log):
    attemps = 1  # number of attemps see(1)
    streamer = FilteredStream(token, log)
    while True:
        try:
            headers = streamer.create_headers()
            rules = streamer.get_rules(headers)
            delete = streamer.delete_all_rules(headers, rules)
            new__rules = streamer.set_rules(headers, delete)
            attemps -= 1
        except:
            var = traceback.format_exc()
            print(var)
        else:
            for _ in range(10):
                try:
                    streamer.get_stream(headers, new_rules)
                except:
                    var = traceback.format_exc()
                    print(var)
                finally:
                    time.sleep(75)
        finally:
            attemps += 1
            time.sleep(n*60)

def updating_connection(token, log):
    requests = 0
    updater = UpdateTweet(token, log)
    
    try:
        while True:
            time.sleep(900)
            headers = updater.create_headers()
            ids = updater.gather_ids()
            for i in range(0, len(ids), 100):
                log.log("Updating process: " + str(round((i/len(ids))*100, 2)) + '%')
                while True:
                    try:
                        updater.update(headers, ids[i:i+100])
                        break
                    except:
                        continue
    except:
        var = traceback.format_exc()
        print(var)

# (1) https://developer.twitter.com/en/docs/twitter-api/rate-limits#v2-limits
