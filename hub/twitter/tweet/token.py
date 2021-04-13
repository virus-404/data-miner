from tool.database import database as db

class Token: 

    def __init__(self, bearer_token, log):
        self.__bearer_token = bearer_token
        self.__log = log
        self.__database = self.__get_database()

     def __get_database(self):
        database = db.Database.get_database_instance()
        self.__log.log('Twitter connection to the database is established')
        database['twitter'].drop_indexes()
        database['twitter'].create_index([("time-stamp", pymongo.ASCENDING)])
        return database['twitter']
