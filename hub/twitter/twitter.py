import os
import xml.etree.ElementTree as ET
from tools.logger import logger
from .filtered_stream import Filtered_stream as FLS

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
    streamer = FLS(keyring.find('bearer-token').text, log)
    headers = streamer.create_headers()
    rules = streamer.get_rules(headers)
    delete = streamer.delete_all_rules(headers, rules)
    set = streamer.set_rules(headers, delete)
    streamer.get_stream(headers, set)
