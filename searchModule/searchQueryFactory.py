from searchModule.api import API
from searchModule.githubRestQuery import GithubRestQuery

class SearchQueryFactory:

    @staticmethod
    def getSearchQuery(queryType, configFile):
        if queryType == API.GithubRest:
            return GithubRestQuery(configFile)
        #TODO Graphql impl
        if queryType == API.GithubGraphQL:
            return None
        return None
