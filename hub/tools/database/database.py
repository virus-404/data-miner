from pymongo import MongoClient
from . import entry 

class Database: 
    """
    A class decorator that creates a database object .
    
    """
    __instance__ = None
    
    def __init__(self):
        if Database.__instance__ is None:
            __instance__ = pymongo.MongoClient()
        else: 
            raise Exception("You cannot create another Database class")
    
    @staticmethod
    def get_database_instance():
        if Database.__instance__ is None: 
            Database()
        else
            return Database.__instance__
    
    @staticmethod
    def write(entry):
        items = entry.get_items()
        for key, value in items:
            sel
