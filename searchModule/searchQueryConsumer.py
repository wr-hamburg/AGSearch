from abc import ABC, abstractmethod

#This class serves as the base for the consumption of a search query.
#Derived classes have to provide actual search, during which the repoNameList
#is supposed to be filled with the repo names. The report at the end also
#has to be supplied by the derived classes.
class SearchQueryConsumer(ABC):
    __slots__=('_searchQuery', '_repoNameList', '_dbCollection')
    
    def __init__(self, searchQuery, databaseCollection):
        self._searchQuery = searchQuery
        self._repoNameList = []
        self._dbCollection = databaseCollection
        
    @abstractmethod
    def startSearch(self):
        pass

    @abstractmethod
    def reportRepos(self):
        pass
