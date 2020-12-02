import os
import importlib
from multiprocessing import Process
from tools import logger as lg

def exec_starter(name):
    social_network = importlib.import_module(name+'.'+name)
    starter = getattr(social_network, 'run')()
    del starter

if __name__ == '__main__':
    logger = lg.Logger('Hub')  # Setting up the logger

    logger.log('Server has started...')
    p = Process(target=exec_starter, args=('twitter',))
    p.start()
    logger.log('Deploying Twitter')

    p.join()
 
 #sort id text timestamp source symbols company_names url verified
