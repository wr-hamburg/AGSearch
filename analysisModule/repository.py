import os
import subprocess
import tempfile
from datetime import datetime

from analysisModule.codeQueryCollection import CodeQueryCollection


# This class represents a singular repository. For initialization, provide the name of the repo, the clone URL
# as well as the path to which the repo will be cloned to, and a CodeQueryCollection. If it is a local repo,
# just don't provide a clone URL and pass the path to the repo as the 'repoPath' argument. In that case the cloning won't happen.
class Repository:
    __slots__ = ("_repoName", "_repoUrl", "_queryCollection")

    def __init__(self, repoName, repoPath, queries, repoUrl=None):
        self._repoName = repoName
        self._repoUrl = repoUrl
        self._queryCollection = queries

    def _cloneRepo(self, repo_path):
        subprocess.check_output(
            f"git clone --depth 1 {self._repoUrl} {repo_path}", shell=True
        )

    def _grepAllQueries(self, tmp_dir):
        self._queryCollection.grepQueries(tmp_dir)

    @property
    def repoName(self):
        return self._repoName

    @property
    def queryCollection(self):
        return self._queryCollection

    def __str__(self):
        res = f"{self._repoUrl}:\n" f"\tQuery Report: "
        queryString = "\t" + str(self._queryCollection)
        res = res + queryString
        return res

    # Use this method to kick off the analysis for the repo
    def analyzeRepository(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            if self._repoUrl != None:
                self._cloneRepo(tmp_dir)
            self._grepAllQueries(tmp_dir)
