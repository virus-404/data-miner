from time import gmtime, strftime
import sys

class Logger:

    def __init__(self, entitie):  # instance attribute
        self.__entitie = '[' + entitie + ']'

    def set_entitie(self, entitie):
        self.__entitie = '[' + entitie + ']'

    def log(self, message):
        time_stamp = strftime(" | %d-%m-%Y; %H:%M:%S | ", gmtime())
        print(self.__entitie + time_stamp + message)
        sys.stdout.flush()
        
#https://stackoverflow.com/questions/616645/how-to-duplicate-sys-stdout-to-a-log-file/3423392#3423392
    
