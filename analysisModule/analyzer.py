import copy
from analysisModule.repository import Repository
from initializerModule.mongoDB import MongoDB

class Analyzer:
    __slots__=('_repos','_queryCollection', '_dbCollection')
    
    def __init__(self, queryCollection, dbCollection):
        self._dbCollection = dbCollection
        self._readReposFromDB()
        self._queryCollection = queryCollection
        
    def _readReposFromDB(self):
        self._repos = []
        for repo in self._dbCollection.getAllEntries():
            analysisRequired = repo.get('analysisRequired')
            repoName = repo.get('_id')
            if not analysisRequired:
                print(f'Skipping {repoName}, not part of this analysis...')
                continue
            repoUrl = repo.get('cloneUrl')
            self._repos.append([repoName, repoUrl])
        
        
    def beginAnalysis(self):
        for repo in self._repos:
            repoName = repo[0]
            repoUrl = repo[1]
            repo = self._analyzeSingleRepository(repoName, repoUrl)
            self._reportSingleRepository(repo)
            del repo
        
    def _analyzeSingleRepository(self, repoName, repoUrl):
        collectionCopy = copy.deepcopy(self._queryCollection)
        #TODO should probably pass an absolute path here instead of just the name
        repo = Repository(repoName=repoName, repoUrl=repoUrl, repoPath='UniqueName', queries=collectionCopy)
        repo.analyzeRepository()
        return repo
      
    def _reportSingleRepository(self, repo):
        self._dbCollection.updateRepoWithFindings(repo)        

