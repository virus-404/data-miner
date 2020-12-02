import os
import importlib
from multiprocessing import Process


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id 0:', os.getpid())

def exec_starter(name):
    social_network = importlib.import_module(name+'.'+name)
    starter = getattr(social_network, 'run')()
    del starter

if __name__ == '__main__':
    info('main line')
    p = Process(target=exec_starter, args=('google',))
    p.start()
    p.join()
 
 #sort id text timestamp source symbols company_names url verified
