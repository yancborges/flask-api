# Modules

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from pymongo import MongoClient

import miscFunctions
import fileFormatting

# Consts

DB_NAME = "test"

# Config

app = Flask(__name__)
app.secret_key='hiddenpass'
app.config["MONGO_URI"] = miscFunctions.loadString()
mongo = PyMongo(app)

client = MongoClient(miscFunctions.loadString())
db = client[DB_NAME]

### Routes

@app.route('/transactions/insert', methods=['POST'])
def trs_insert():
	if( request.method == 'POST' ):
		try:
			content = request.get_json()
			if(fileFormatting.validateFormat(content,'transactions')):
				result = db['transactions'].insert_one(content)
				return jsonify({"status": "success"})
			else:
				return jsonify({"status": "error", "message": miscFunctions.errorCodes(2)})
			
		except:
			return jsonify({"status": "error", "message": miscFunctions.errorCodes(1)})

@app.route('/transactions/get', methods=['GET'])
def trs_get():
	if( request.method == 'GET'):
		try:
			data = db['transactions'].find()
			return jsonify(miscFunctions.vectorize(data))
		except:
			return jsonify({"status": "error", "message": miscFunctions.errorCodes(1)})

@app.route('/transactions/patch', methods=['PATCH'])
def trs_patch():
	if( request.method == 'PATCH'):
		try:
			content = request.get_json()
			if(fileFormatting.validateFormat(content,'transactions')):
				result = db['transactions'].update_one({'Id': content['Id']}, {'$set': content})
				count = result.modified_count
				return jsonify({"status": "success", "modified_documents": count})
			else:
				return jsonify({"status": "error", "message": miscFunctions.errorCodes(2)})
		except:
			return jsonify({"status": "error", "message": miscFunctions.errorCodes(1)})

@app.route('/transactions/delete', methods=['DELETE'])
def trs_delete():
	if( request.method == 'DELETE'):
		try:
			content = request.get_json()
			if(fileFormatting.validateFormat(content, 'transactions')):
				result = db['transactions'].delete_one({'Id': content['Id']})
				count = result.deleted_count
				return jsonify({"status": "success", "deleted_documents": count})
			else:
				return jsonify({"status": "error", "message": miscFunctions.errorCodes(2)})
		except:
			return jsonify({"status": "error", "message": miscFunctions.errorCodes(1)})

@app.route('/transactions/search', methods=['POST'])
def trs_search():
	if( request.method == 'POST'):
		try:
			content = request.get_json()
			if(fileFormatting.validateFormat(content, 'transactions')):
				data = db['transactions'].find(
					{
						"DataHora": { "$gte": content["DataHora"] },
						"Valor": { "$gte": content["Valor"] }
					}
				)
				return jsonify(miscFunctions.vectorize(data))
			else:
				return jsonify({"status": "error", "message": miscFunctions.errorCodes(2)})
		except:
			return jsonify({"status": "error", "message": miscFunctions.errorCodes(1)})

@app.route('/')
def index():
	return 'Welcome, its working!'

# Running

if __name__ == '__main__':
    app.secret_key='hiddenpass'
    app.run(debug=True)

