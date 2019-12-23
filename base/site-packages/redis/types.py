class Base(object):
    def __init__(self, key):
        self.key = key
        
    def encode(self, value):
        return value
        
    def decode(self, value):
        return value
        
    def rename(self, key, force=False):
        pass
        
    def delete(self):
        pass
        
    def expire(self, timeout):
        pass
        
    def expires(self):
        pass
        
        

class Key(Base):
    def __init__(self, key, value=None):
        super(Key, self).__init__(key)
        if value is not None:
            self.set(value)
        
    def get(self):
        pass
        
    def set(self, value):
        pass
        
    def setdefault(self, value):
        pass
        
    def increment(self, by=1):
        pass
        
    def decrement(self, by=1):
        pass
        
        
class List(Base):
    def __init__(self, key, value=None, start=None, end=None):
        super(List, self).__init__(key)
        if value is not None:
            if start is not None or end is not None:
                raise TypeError("Cannot specify a value to save and a start/end boundary")
            if not hasattr(value, '__iter__'):
                raise TypeError("The value passed to List() must be iterable")
            # TODO PIPE THIS
            for item in value:
                self.append(item)
        self._start = start
        self._end = end
        
    def __len__(self):
        pass
        
    def __getitem__(self, index):
        # if index is an instance of a slice, return a new List() with boundaries set
        if isinstance(index, slice):
            return List(self.key, start=index.start, end=index.end)
        elif isinstance(index, (int, long)):
            # TODO RETURN ITEM AT INDEX
            pass
        raise TypeError("List indices must be integers")
        
    def __setitem__(self, index, value):
        # if value is another List(), use pipelining to set the current list?
        # if index is a slice, then replace that slice w/ the value, again using pipelining.
        pass
        
    def __delitem__(self, index):
        pass
        
    def __iter__(self):
        pass
        
    def append(self, value):
        pass
        
    def insert(self, index, value):
        pass
        
    def pop(self, index=None):
        pass
        
    
        
    
        
    
    
class Set(Base):
    pass
    
class SortedSet(Base):
    pass
    