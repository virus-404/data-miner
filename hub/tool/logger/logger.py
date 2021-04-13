from time import gmtime, strftime
import sys

class Logger:

    def __init__(self, ssnn):  # instance attribute
        self.__ssnn = '[' + ssnn + ']'

    def set_ssnn(self, ssnn):
        self.__ssnn = '[' + ssnn + ']'

    def log(self, message):
        time_stamp = strftime(" | %d-%m-%Y; %H:%M:%S | ", gmtime())
        print(self.__ssnn + time_stamp + message)
        sys.stdout.flush()
        
#https://stackoverflow.com/questions/616645/how-to-duplicate-sys-stdout-to-a-log-file/3423392#3423392
    
