import pymongo
from tool.database import database as db

class Token: 

    def __init__(self, bearer_token, log):
        self.bearer_token = bearer_token
        self.log = log
        self.database = self.__get_database()

    def __get_database(self):
        database = db.Database.get_database_instance()
        self.log.log('Twitter connection to the database is established')
        database['twitter'].drop_indexes()
        database['twitter'].create_index([("time-stamp", pymongo.ASCENDING)])
        return database['twitter']
