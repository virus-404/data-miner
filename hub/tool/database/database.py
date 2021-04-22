import os
from pymongo import MongoClient, errors
from tool.logger import logger as lg
from dataclasses import dataclass


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
                ddbb = MongoClient(os.environ['URI']).get_database() # get_database with no "name" argument chooses the DB from the URI
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
            self.database.create_collection('twitter')
        except errors.CollectionInvalid as exist:
            messages.append(str(exist))

        try:
            self.database.create_collection('youtube')
        except errors.CollectionInvalid as exist:
            messages.append(str(exist))

        try:
            self.database.create_collection('google')
        except errors.CollectionInvalid as exist:
            messages.append(str(exist))

        try:
            self.database.create_collection('facebook')
        except errors.CollectionInvalid as exist:
            messages.append(str(exist))

        try:
            self.database.create_collection('reddit')
        except errors.CollectionInvalid as exist:
            messages.append(str(exist))

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
