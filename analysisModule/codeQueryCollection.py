import subprocess
from analysisModule.codeQuery import CodeQuery

#This class serves as a collection of the single code queries and does the heavy lifting regarding 
#the greps.
class CodeQueryCollection:
    __slots__=('_queries')

    def __init__(self, listOfQueryStrings):
        self._queries = []
        for q in listOfQueryStrings:
            self.addQuery(q)
        
    def addQuery(self, queryString):
        self._queries.append(CodeQuery(queryString))
    
    def grepQueries(self, repoPath):
        for query in self._queries:
            res = subprocess.check_output(f'grep -RnwIi ".*{query.query}.*" {repoPath} | wc -l', shell=True)
            countForCurrentRepo = int(res.decode('utf-8'))
            query.updateCount(countForCurrentRepo)
    
    @property   
    def queries(self):
        return self._queries
        
    def __str__(self):
        res = ''
        for q in self._queries:
            res = res + str(q) + " "
        return res
        
    def __iter__(self):
        return iter(self._queries)

