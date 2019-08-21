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