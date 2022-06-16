from searchModule.searchQuery import SearchQuery
from searchModule.configValidity import ConfigValidity

#Class for the creation of a query usable by Pygithub (for the REST API).
class GithubRestQuery(SearchQuery):
    def __init__(self, configFile):
        super().__init__(configFile)
        self._searchQuery = self._createQueryFromConfigFile()
        
    def _createQueryFromConfigFile(self):
        fileHandle = open(self._configFile, 'r')
        fileContent = fileHandle.readlines()
        fileHandle.close()
        configDict = ConfigValidity.createDictFromContent(fileContent)
        queryString = ''
        for key,value in configDict.items():
            for element in value:
                queryString = queryString + self._transformToQueryParameter(key, element)
        if len(queryString) > 256:
            raise RuntimeError(f'Query too long, limit is 256 (query is at {len(queryString)})')
        return queryString
        
    def _transformToQueryParameter(self, key, value):
        #TODO If the parameter transformation is similar across multiple APIs, consider creating some extra classes for that purpose
        #Could do this in if else right now as well instead of self-made switch
        switch={
            'language':f'language:{value} ',
            'keyword':f'{value} ',
            'pushed':f'pushed:{value} ',
            'stars':f'stars:{value} ',
            'topic':f'topic:{value} '
        }
        return switch.get(key)

