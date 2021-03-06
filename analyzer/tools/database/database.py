import os
from pymongo import MongoClient, errors
from tools.logger import logger as lg
from dataclasses import dataclass
from frozendict import frozendict

@dataclass(frozen=True)
class Database: 
    """
    A class decorator that creates a database object .
    
    """
    __instance = None
    
    database = None
    logger = None
    __key = object()
    
    def __init__(self, key):
        assert (key == Database.__key), \
        "Database objects must be created using Database.get_database_instance (!)"
        
        if Database.__instance is None:
            try:
                ddbb = frozendict({
                    'intelligence': MongoClient(os.environ['URI']).get_database(),
                    'social_networks': MongoClient(os.environ['URI2']).get_database()
                }) # get_database with no "name" argument chooses the DB from the URI
                object.__setattr__(self, 'database', ddbb)
            except errors.ConnectionFailure as connection:
                raise Exception("Connection to the database failed (!)")
            else:
                object.__setattr__(self,'logger', lg.Logger('Database'))
                self.__insert_collections()
                Database.__instance = ddbb
        else: 
            raise Exception("There was no connection to the database (!)")

    def __insert_collections(self):
        messages = []

        try:
            self.database['intelligence'].create_collection(
                'twitter_sentiment_analysis')
        except errors.CollectionInvalid as exist:
            messages.append(str(exist).capitalize())

        if len(messages) == 0: 
            messages.append('All collections were created successfully !')

        for message in messages:
            self.logger.log(message)

    @staticmethod
    def get_database_instance():
        if Database.__instance is None: 
            Database(Database.__key)
            assert (Database.__instance is not None), "Database is None (!)"
        return Database.__instance

#https://stackabuse.com/the-singleton-design-pattern-in-python/
