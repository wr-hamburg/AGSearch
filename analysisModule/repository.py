import os
import subprocess
from datetime import datetime
from analysisModule.codeQueryCollection import CodeQueryCollection


#This class represents a singular repository. For initialization, provide the name of the repo, the clone URL
#as well as the path to which the repo will be cloned to, and a CodeQueryCollection. If it is a local repo,
#just don't provide a clone URL and pass the path to the repo as the 'repoPath' argument. In that case the cloning won't happen.
class Repository:
    __slots__=('_repoName', '_repoUrl', '_queryCollection', '_repoPath')

    def __init__(self, repoName, repoPath, queries, repoUrl=None):
        self._repoName = repoName
        self._repoUrl = repoUrl
        self._queryCollection = queries
        self._repoPath = repoPath
                
    def _cloneRepo(self):
        if os.path.isdir(self._repoPath):
            subprocess.check_output(f'rm -rf {self._repoPath}', shell=True)
        subprocess.check_output(f'git clone --depth 1 {self._repoUrl} {self._repoPath}', shell=True)
        
    def _removeRepo(self):
        subprocess.check_output(f'rm -rf {self._repoPath}', shell=True)
        
    def _grepAllQueries(self):
        self._queryCollection.grepQueries(self._repoPath)
        
    @property
    def repoName(self):
        return self._repoName
        
    @property
    def queryCollection(self):
        return self._queryCollection
    
    def __str__(self):
        res = f"{self._repoUrl}:\n"\
        f"\tQuery Report: "
        queryString = '\t' + str(self._queryCollection)
        res = res + queryString
        return res
    
    #Use this method to kick off the analysis for the repo    
    def analyzeRepository(self):
        if self._repoUrl != None:
            self._cloneRepo()
        self._grepAllQueries()
        if self._repoUrl != None:
            self._removeRepo()

