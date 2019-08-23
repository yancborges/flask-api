# Modules

import json
from jsonschema import validate

# Schemas

TRANSACTION_SCHEMA = {
	"DataHora": "timestamp",
    "id": "string",
    "ContaInicial": "double",
    "ContaFinal": "double",
    "Valor": "double"
}

# Functions

def validateFormat(file,page):
	if(isJson(file)):
		validate(instance=file,schema=getSchema(page))
		return True
	else:
		return False

def isJson(file):
	try:
		jd = json.dumps(file)
		#jo = json.loads(file)
		return True
	except Exception as e:
		print(e)
		return False

def getSchema(page):
	if(page == 'transactions'):
		return TRANSACTION_SCHEMA


