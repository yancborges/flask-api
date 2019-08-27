# Modules

import json
from jsonschema import validate

# Schemas

# Both ways i tried seems to not work.
# Invalid formatted documents are allowed to be inserted for some reason i dont know.

'''
TRANSACTION_SCHEMA = {
	"DataHora": "timestamp",
    "id": "string",
    "ContaInicial": "double",
    "ContaFinal": "double",
    "Valor": "double"
}'''

TRANSACTION_SCHEMA = {
	"type": "object",
	"properties": {
		"DataHora": {"type": "number"},
    	"Id": {"type": "string"},
    	"ContaInicial": {"type": "number"},
    	"ContaFinal": {"type": "number"},
    	"Valor": {"type": "number"}
	},
	"additionalProperties": False
}

# Functions

def validateFormat(file,page):
	if(isJson(file)):
		try:
			validate(instance=file,schema=getSchema(page))
		except:
			return False
		return True
	return False

def isJson(file):
	try:
		jd = json.dumps(file)
		#jo = json.loads(file)
		return True
	except:
		return False

def getSchema(page):
	schemas = {
		"transactions": TRANSACTION_SCHEMA,
	}
	return schemas[page]
		


