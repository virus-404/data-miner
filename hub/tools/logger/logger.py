from time import gmtime, strftime

class Logger:

    # instance attribute
    def __init__(self, ssnn):
        self.__ssnn = '[' + ssnn + ']'

    def set_ssnn(self, ssnn):
        self.__ssnn = '[' + ssnn + ']'

    def log(self, message):
        time_stamp = strftime(" | %d-%m-%Y; %H:%M:%S | ", gmtime())

        print(self.__ssnn + time_stamp + message)
        
#https://stackoverflow.com/questions/616645/how-to-duplicate-sys-stdout-to-a-log-file/3423392#3423392
    
