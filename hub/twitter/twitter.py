import os
import time
import traceback
from tool.logger import logger

import xml.etree.ElementTree as ET
from .tweet.filtered_stream import FilteredStream 

def set_up():
    cwd = os.getcwd()  # Get the current working directory (cwd)
    os.chdir(cwd + '/twitter')  # Settig the root directory for the file
    return logger.Logger('Twitter') # Setting up the logger
    
def run():
    log = set_up()
    log.log('Twitter setting up')
    log.log('Reading credentials')
    keys = ET.parse('files/keys.xml')
    keyring = keys.getroot()
    streamer = FilteredStream(keyring.find('bearer-token').text, log)
    import sys
    sys.exit()
    n = 1 # number of attemps

    
    while True:
        try:
            headers = streamer.create_headers()
            rules = streamer.get_rules(headers)
            delete = streamer.delete_all_rules(headers, rules)
            set = streamer.set_rules(headers, delete)
            n -=1
        except:
            var = traceback.format_exc()
            print (var)
        else:
            for _ in range(10):
                try:
                    streamer.get_stream(headers, set)
                except :
                    var = traceback.format_exc()
                    print(var)
                finally: 
                    time.sleep(75)
        finally:
            n += 1           
            time.sleep(n*60)


