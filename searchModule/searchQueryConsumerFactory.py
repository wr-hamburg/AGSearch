from searchModule.api import API
from searchModule.githubRestConsumer import GithubRestConsumer

class SearchQueryConsumerFactory:

    @staticmethod
    def getConsumer(consumerType, query, db):
        if consumerType == API.GithubRest:
            return GithubRestConsumer(query, db)
        if consumerType == API.GithubGraphQL:
            raise NotImplementedError("graphQL consumer has not been implemented yet")
        return None
