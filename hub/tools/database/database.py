import os
from pymongo import MongoClient, errors
from tools.logger import logger as lg

class Database: 
    """
    A class decorator that creates a database object .
    
    """
    __instance = None
    __logger = None
    __key = object()
    
    def __init__(self, key):
        assert (key == Database.__key), \
         "Database objects must be created using Database.get_database_instance (!)"
        
        if Database.__instance is None:
            try:
                self.__instance = MongoClient(
                    os.environ['URI']).get_database()
            except errors.ConnectionFailure as connection:
                raise Exception("Connection to the database failed (!)")
            else:
                self.__logger = lg.Logger('Database')
                self.__insert_collections()
        else: 
            raise Exception("There was no connection to the database (!)")
    

    def __insert_collections(self):
        messages = []
        try:
            self.__instance.create_collection('twitter')
        except errors.CollectionInvalid as exist:
            messages.append(str(exist))

        try:
            self.__instance.create_collection('youtube')
        except errors.CollectionInvalid as exist:
            messages.append(str(exist))

        try:
            self.__instance.create_collection('google')
        except errors.CollectionInvalid as exist:
            messages.append(str(exist))

        try:
            self.__instance.create_collection('reddit')
        except errors.CollectionInvalid as exist:
            messages.append(str(exist))

        if len(messages) == 0: 
            messages.append('All collections were created successfully !')

        for message in messages:
            self.__logger.log(message)

    @staticmethod
    def get_database_instance():
        if Database.__instance is None: 
            Database(Database.__key)
        else:
            return Database.__instance

    
    def insert_document(self, ssnn, document):
        

    def update_document(self, ssnn, document):
        pass

    def delete_document(self, ssnn, document):
        pass

    def get_document(self, ssnn, document):
        pass
