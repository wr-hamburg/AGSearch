import pymongo

from analysisModule.codeQuery import CodeQuery
from analysisModule.codeQueryCollection import CodeQueryCollection
from searchModule.githubMetadata import GithubMetadata


# TODO apply Singleton pattern
class MongoDB:

    __slots__ = "_collection"

    # TODO if client can change port, change port here
    def __init__(self, collectionName):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        database = client["githubToolDB"]
        self._collection = database[collectionName]

    # Used for the initial entry of a repo (upon returning from the search query)
    def initializeRepo(self, repoName, metadata):
        if self._collection.find_one({"_id": repoName}):
            print(f"{repoName} already in Collection, not updating metadata...")
            return
        repoDict = {"_id": repoName, "analysisRequired": True}
        repoDict.update(metadata.__dict__)
        self._collection.insert_one(repoDict)

    # Used to fill in the results from the code search for all the repos
    def updateRepoWithFindings(self, repo):
        repoName = repo.repoName
        queryCollection = repo.queryCollection
        repoQuery = {"_id": repoName}
        dbObject = self._collection.find_one(repoQuery)

        if not dbObject:
            print(f"{repoName} not in DB, adding it now...")
        elif not dbObject.get("analysisRequired"):
            print(f"{repoName} not part of this query, skipping...")
            return

        dbDict = {}
        for query in queryCollection:
            singleDict = {query.query: query.totalCount}
            dbDict.update(singleDict)
        dbDict.update({"analysisRequired": False})

        self._collection.update_one(repoQuery, {"$set": dbDict}, upsert=True)

    def getAllEntries(self):
        return self._collection.find()
