#This class represents a single code query. It essentially just encapsulates the counter for each
#query string.

class CodeQuery:
    __slots__ = ('_query', '_totalCount')

    def __init__(self, query):
        self._query = query
        self._totalCount = 0
        
    def updateCount(self, count):
        self._totalCount = self._totalCount + count
    
    @property        
    def query(self):
        return self._query
    
    @property
    def totalCount(self):
        return self._totalCount
        
    def __str__(self):
        return f'{self._query}={self._totalCount}'

