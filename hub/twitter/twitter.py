import os
import xml.etree.ElementTree as ET
from tools import logger as lg

def run():
    cwd = os.getcwd()  # Get the current working directory (cwd)
    os.chdir(cwd + '/twitter')  # Settig the root directory for the file
    logger = lg.Logger('Twitter') # Setting up the logger

    keys = ET.parse('keys.xml')
    keyring = keys.getroot()
    
    logger.log(keyring.find('api-key').text)
