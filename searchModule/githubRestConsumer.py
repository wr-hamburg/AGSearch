from github import Github
import os
import time
import re
from datetime import datetime, timezone, timedelta
from searchModule.searchQueryConsumer import SearchQueryConsumer
from searchModule.githubMetadata import GithubMetadata

#This class consumes a REST query. Since we are working with Github repos, we also
#fetch metadata that could be of interest.
class GithubRestConsumer(SearchQueryConsumer):
    __slots__=('_githubObject', '_githubMetadataDict')

    def __init__(self, searchQuery, dbCollection):
        super().__init__(searchQuery, dbCollection)
        github_key = os.getenv('GITHUB_KEY')
        if not github_key:
            raise RuntimeError('Please provide a Github token in the environment variable GITHUB_KEY')
        self._githubObject = Github(github_key)
        self._githubMetadataDict = {}
        
    #One search only returns up to 1000 elements (limit imposed by Github). To be able to
    #find more than that the search is split into multiples, each covering a different
    #range regarding the time of the last push.
    def startSearch(self):
        nextQuery = self._searchQuery.searchQuery
        if 'pushed:' not in nextQuery:
            now = datetime.today()
            timeString = now.strftime('%Y-%m-%dT%H:%M:%SZ')
            nextQuery = nextQuery + f'pushed:<{timeString} '
        self._recursiveSearch(nextQuery)

        
    def _waitIfNecessary(self):
        #In testing, the searches sometimes blew through the search rate limit,
        #decrementing the counter by multiples at once (don't know why, but related to
        #how the search is implemented in pygithub). It's probably not going
        #happen anymore, but if it does, just raise the '0' below to 5 or something.
        rateLimit = self._githubObject.get_rate_limit().search
        if rateLimit.remaining == 0:
            reset = rateLimit.reset.replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            seconds = abs((reset-now).total_seconds())
            print(f'Waiting {seconds} seconds, due to {rateLimit}')
            time.sleep(seconds)
            
    def _recursiveSearch(self, nextQuery):
        self._waitIfNecessary()
        print(f'Issuing query {nextQuery}')
        repos = self._githubObject.search_repositories(nextQuery, sort='updated', order='desc')
        total = repos.totalCount
        if total == 1000:
            #repos[999] literally breaks the search limit most of the time, even from 30/30 remaining calls.
            #Page 33, element 9 is the 1000th element and should be the last one that is accessible, however
            #due to the implementation of the search in pygithub the 33rd page can contain 30 elements, if
            #there are at least 1020 elements. However, we can't really rely on that and checking it in a
            #reliable fashion also seems impossible (correct me if I'm wrong though). So for consistency's
            #sake, we will consider the 1000th element as the last one returned from our search.
            self._waitIfNecessary()
            lastRepo = repos.get_page(33)[9]
            #Subtracting 1 second from the timestamp to exclude the responsible repo from next search
            pushDate = lastRepo.pushed_at - timedelta(seconds=1)
            timeString = pushDate.strftime('%Y-%m-%dT%H:%M:%SZ')
            nextQuery = self._determineNextTimeQuery(nextQuery, timeString)
            self._recursiveSearch(nextQuery)
            
        #Can't use 'for each' due to consistency problem explained above
        for i in range(total):
            self._waitIfNecessary()
            fullName = repos[i].full_name
            self._repoNameList.append(fullName)
            cloneUrl = repos[i].clone_url
            starCount = repos[i].stargazers_count
            pushDate = repos[i].pushed_at
            githubMetadata = GithubMetadata(stars=starCount, cloneUrl=cloneUrl, pushDate=pushDate)
            self._githubMetadataDict[fullName] = githubMetadata
            
    #Takes the previous query and determines what kind of query it was (<,>,..)
    #Depending on that, a new query is created, keeping any relevant boundaries.
    #(Reminder: 'pushed:<time' finds all repos which were last pushed to BEFORE that time)
    def _determineNextTimeQuery(self, previousQuery, timeString):
        lessThan = re.search('pushed:<.* ', previousQuery)
        if lessThan:
            return re.sub(lessThan.group(), f'pushed:<{timeString} ', previousQuery)
        
        greaterThan = re.search('pushed:>.* ', previousQuery)
        if greaterThan:
            group = greaterThan.group()
            lowerBoundary = group[8:-1]
            
        rangeQuery = re.search('pushed:.*\\.\\..* ', previousQuery)
        if rangeQuery:
            group = rangeQuery.group()
            positionOfFirstDot = group.find('.')
            lowerBoundary = group[7:positionOfFirstDot]
            
        return re.sub(group, f'pushed:{lowerBoundary}..{timeString} ', previousQuery)
    
           
    def reportRepos(self):
        for name in self._repoNameList:
            metadata = self._githubMetadataDict[name]
            self._dbCollection.initializeRepo(name, metadata)

