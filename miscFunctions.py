# Loading connect string from local file
def loadString():
	with open('mongo_string.txt') as f:
		return f.read()

def errorCodes(code):
	
	if(code == 1):
		return 'Something gone wrong'
	elif(code == 2):
		return 'Error: Wrong format'
	else:
		return 'success'


# Creating a list with objects in mongo cursor
def vectorize(obj):
	arr = []
	for item in obj:
		
		# IMPORTANT!

		# As the mongo ObjetcId is not JSON serializable, i had to took it off from the array.
		# Some issues at internet has been solved using 'bson' module,
		# however, it crashed my pymongo, so, as the document requested has an 'Id'	value,
		# i decided to remove the mongo Id while i look for a better way.
		item.pop('_id')

		arr.append(item)
	return arr