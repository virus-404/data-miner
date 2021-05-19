import os
import sys
import importlib
import pathlib
import multiprocessing as mp
from tools.logger import logger as lg 
from tools.database import database as db 

def exec_starter(name):
    social_network = importlib.import_module(name+'.'+name)
    starter = getattr(social_network, 'run')()
    del starter

if __name__ == '__main__':
    logger = lg.Logger('Hub')  # Setting up the logger + greetings
    logger.log('Server has started...') 
    logger.log('Python version : ' + str(sys.version))
    logger.log('Server is creating the database...')

    mp.set_start_method('fork')
    logger.log('All the processes are started with ' + mp.get_start_method() + ' method')
  
    p = mp.Process(target=exec_starter, args=('twitter',))
    logger.log('Deploying Twitter')
    p.start()
    p.join()

    # testdb = db.Database.get_database_instance()
    # res = testdb.database.twitter.insert_one({'succes': ':D', 'user': 'test1'})
    # logger.log(str(res.inserted_id))
    
    # res = testdb.database.twitter.delete_one({'_id': res.inserted_id})
    # logger.log(str(res.deleted_count))
 
