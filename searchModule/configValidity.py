#This class checks whether or not the supplied config files contains proper keys and transforms them into a usable dict.
class ConfigValidity:

	#The accepted keys from the config file. TODO Solution seems suboptimal, should probably refactor that at some point.
	#'pushed' has to be supplied as YYYY-MM-DD.
	#Both 'stars' and 'pushed' can be specified as a range (value1..value2) or with '<' or '>'
	acceptedKeys = ['keyword', 'language', 'stars', 'pushed', 'topic']

	#Creates a dictionary from the config file. Each key is associated with a list of values. The values are expected
	#in a comma-separated list inside of the config file. TODO Should probably indicate that somewhere.
	@staticmethod
	def createDictFromContent(content):
	    result = {}
	    for line in content:
	        key = line.split(':')[0]
	        if key not in ConfigValidity.acceptedKeys:
	            raise ValueError
	        valuesStripped = line.split(':')[1].strip(' \n')
	        valueList = []
	        for value in valuesStripped.split(','):
	            valueList.append(value)
	        result[key] = valueList
	    return result
