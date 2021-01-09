from ABC import ABCMeta, abstractmethod

class Entry(ABCMeta):

    def __subclasshook__(self,subclass):
        return (hasattr(subclass, 'get_items') and
                callable(subclass.get_items) or
                NotImplemented)
        
    @abstractmethod
    def get_items(self):
        """Get all items in the collection """
        raise NotImplementedError

#https://realpython.com/python-interface/
