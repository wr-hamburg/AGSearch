from abc import ABC, abstractmethod

#Abstract class for the search queries. Each query takes an input file from
#which it creates the search query. Since each search query looks different
#(REST, GraphQL etc) the creation of the query is abstract.
class SearchQuery(ABC):
    __slots__=('_searchQuery', '_configFile')

    def __init__(self, configFile):
        self._searchQuery = None
        self._configFile = configFile
    
    @property
    def searchQuery(self):
        return self._searchQuery
        
    @abstractmethod
    def _createQueryFromConfigFile(self):
        pass

