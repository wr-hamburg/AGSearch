from enum import Enum, auto

#Update this enum if any new APIs are added (ie Sourceforge)
class API(Enum):
    GithubRest = auto()
    GithubGraphQL = auto()
