from analysisModule.codeQueryCollection import CodeQueryCollection

class CodeQueryReader:

    @staticmethod
    def readCodeQueriesFromFile(filepath):
        codeQueryFile = open(filepath, 'r')
        codeQueriesContent = codeQueryFile.readlines()
        codeQueryFile.close()
        codeQueryList = []
        for line in codeQueriesContent:
            codeQueryList.append(line.strip('\n'))
        return CodeQueryCollection(codeQueryList)

