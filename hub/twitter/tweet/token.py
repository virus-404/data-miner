import pymongo
from abc import ABC, abstractmethod
from tools.database import database as db

class Token(ABC): 

    def __init__(self, bearer_token, log):
        self.bearer_token = bearer_token
        self.log = log
        self.database = self.__get_database()

    def __get_database(self):
        database = db.Database.get_database_instance()
        collections = {}

        self.log.log('Twitter connection to the database is established')
        database['twitter'].drop_indexes()
        database['twitter'].create_index([('created_at', pymongo.ASCENDING)])
        collections['twitter'] = database['twitter']

        database['twitter_users'].drop_indexes()
        database['twitter_users'].create_index([('id', pymongo.ASCENDING)])
        collections['twitter_users'] = database['twitter_users']

        return collections

    @abstractmethod
    def create_headers(self):
        headers = {"Authorization": "Bearer {}".format(self.bearer_token)}
        return headers
