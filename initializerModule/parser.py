import argparse

from searchModule.api import API


# TODO user arguments: port for container?
# This class parses user input. If you wish to extend this, just add a new argument and return it inside of the dict at the end.
# The dict currently contains the path to both files, the name for the DB collection and the API.
class Parser:

    @staticmethod
    def parseInput():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--searchconfig",
            required=True,
            help="Path to the file containing the search config information",
        )
        parser.add_argument(
            "--codequeries",
            required=True,
            help="Path to the file containing the code query information",
        )
        parser.add_argument(
            "--dbcollection",
            nargs="?",
            default="veryGoodName",
            help="optional name for the DB collection",
        )
        # If any APIs get added, modify the choices below and the addition to the result
        parser.add_argument(
            "--api",
            nargs="?",
            default="rest",
            choices=["rest", "graphql"],
            help="Specify search API (REST or GraphQL)",
        )

        args = parser.parse_args()

        results = {}
        results.update({"searchconfig": args.searchconfig})
        results.update({"codequeries": args.codequeries})
        results.update({"dbcollection": args.dbcollection})
        if args.api == "rest":
            results.update({"api": API.GithubRest})
        elif args.api == "graphql":
            results.update({"api": API.GithubGraphQL})
        return results
