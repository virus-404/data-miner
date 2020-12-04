import os
import xml.etree.ElementTree as ET
from tools import logger as lg
from .filtered_stream import Filtered_stream as FLS

def set_up():
    cwd = os.getcwd()  # Get the current working directory (cwd)
    os.chdir(cwd + '/twitter')  # Settig the root directory for the file
    return lg.Logger('Twitter') # Setting up the logger

def run():
    logger = set_up()
    logger.log('Twitter starts conection ...')

    keys = ET.parse('keys.xml')
    keyring = keys.getroot()
    streamer = FLS(keyring.find('bearer-token').text)
    
    headers = streamer.create_headers()
    rules = streamer.get_rules(headers)
    delete = streamer.delete_all_rules(headers, rules)
    set = streamer.set_rules(headers, delete)
    """get_stream(headers, set)  """
