import os
import time
import traceback
from tool.logger import logger

import xml.etree.ElementTree as ET
from .tweet.filtered_stream import FilteredStream 
from .tweet.update_tweet import UpdateTweet

'''
    Beacuse the API is not giving the mterics of the tweets. The hub needs first the filtered tweet, and then gather the organic metrics.
        -   streaming:  getting filtered streams accordding to the filtered keywords of the folder file.
        -   updating:   getting tweets metrics by sending id.
    It needs to be used first in streaming mode and then in updating mode. 
'''
mode = 'updating' 

def set_up():
    cwd = os.getcwd()  # Get the current working directory (cwd)
    os.chdir(cwd + '/twitter')  # Settig the root directory for the file
    return logger.Logger('Twitter') # Setting up the logger
    
def run():
    log = set_up()
    log.log('Twitter setting up')
    keys = ET.parse('files/keys.xml')
    keyring = keys.getroot()
    log.log('Reading credentials')
    log.log(mode + 'is on')

    if mode == 'streaming':
        streaming_connection(keyring.find('bearer-token').text, log)
    else: 
        updating_connection(keyring.find('bearer-token').text, log)
  

def streaming_connection(token, log):
    attemps = 1  # number of attemps see(1)
    streamer = FilteredStream(token, log)
    while True:
        try:
            headers = streamer.create_headers()
            rules = streamer.get_rules(headers)
            delete = streamer.delete_all_rules(headers, rules)
            set = streamer.set_rules(headers, delete)
            attemps -= 1
        except:
            var = traceback.format_exc()
            print(var)
        else:
            for _ in range(10):
                try:
                    streamer.get_stream(headers, set)
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
        headers = updater.create_headers()
        ids = updater.gather_ids()
        for i in range(0, len(ids), 100):
            updater.update(headers, ids[i:i+100])
            

    except:
        var = traceback.format_exc()
        print(var)


'''
 for id in updater.id_list:
        requests += updater.update(id)

        # 900 requests per 15-minute window (user auth) see(1)
        if requests == 900: 
            requests = 0
            time.sleep(900)

>> for doc in db.test.find():
...     print(doc)
...
{u'x': 1, u'_id': 0}
{u'x': 1, u'_id': 1}
{u'x': 1, u'_id': 2}
>> result = db.test.update_one({'x': 1}, {'$inc': {'x': 3}})
>> result.matched_count
1
>> result.modified_count
1


 (1) https://developer.twitter.com/en/docs/twitter-api/rate-limits#v2-limits

'''
