from pymongo import MongoClient

class Database: 
    #Singleton pattern 

    __instance__ = None
    
    def __init__(self):
        if Database.__instance__ is None:
            __instance__ = pymongo.MongoClient("localhost", 27017)
        else: 
            raise Exception("You cannot create another Database class")
    
    @staticmethod
    def get_database_instance():
        if Database.__instance__ is None: 
            Database()
        else
            return Database.__instance__
    



      
 
