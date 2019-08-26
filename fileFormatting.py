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

TRANSACTION_SCHEMA_POST = {
	"type": "object",
	"properties": {
		"DataHora": {"type": "number"},
    	"Id": {"type": "string"},
    	"ContaInicial": {"type": "number"},
    	"ContaFinal": {"type": "number"},
    	"Valor": {"type": "number"}
	}
}

TRANSACTION_SCHEMA_PATCH = {
	"type": "object",
	"properties": {
		"DataHora": {"type": "number"},
    	"Id": {"type": "string"},
    	"ContaInicial": {"type": "number"},
    	"ContaFinal": {"type": "number"},
    	"Valor": {"type": "number"}
	}
}

TRANSACTION_SCHEMA_DELETE = {
	"type": "object",
	"properties": {
		"Id": {"type": "string"}
	}
}

TRANSACTION_SCHEMA_SEARCH = {
	"type": "object",
	"properties": {
		"DataHora": {"type": "number"},
    	"Valor": {"type": "number"}
	}
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
		"transactions_post": TRANSACTION_SCHEMA_POST,
		"transactions_patch": TRANSACTION_SCHEMA_PATCH,
		"transactions_delete": TRANSACTION_SCHEMA_DELETE,
		"transactions_search": TRANSACTION_SCHEMA_SEARCH
	}
	return schemas[page]
		


