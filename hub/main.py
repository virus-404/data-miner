import os
import sys
import importlib
import pathlib
import multiprocessing as mp
from tools import logger as lg


def exec_starter(name):
    social_network = importlib.import_module(name+'.'+name)
    starter = getattr(social_network, 'run')()
    del starter

if __name__ == '__main__':
    logger = lg.Logger('Hub')  # Setting up the logger + greetings
    logger.log('Server has started...') 
    logger.log('Server is creating the database...')
    setup_database()

    logger.log('Pythone version : ' + str(sys.version))

    mp.set_start_method('fork')
    logger.log('All the processes are started with ' + mp.get_start_method() + ' method')
    
    #p = mp.Process(target=exec_starter, args=('twitter',))
    #p.start()
    #logger.log('Deploying Twitter')
    #p.join()
 
 #sort id text timestamp source symbols company_names url verified
