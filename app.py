# Modules

from flask import Flask, request, jsonify, make_response
from flask_pymongo import PyMongo
import jwt
from pymongo import MongoClient

from functools import wraps

import miscFunctions
import fileFormatting

# Consts

DB_NAME = "test"
USER_PASSWORD = '123'

# Config

app = Flask(__name__)
app.secret_key='hiddenpass'
app.config["MONGO_URI"] = miscFunctions.loadString()
mongo = PyMongo(app)

client = MongoClient(miscFunctions.loadString())
db = client[DB_NAME]

### Auth

@app.route('/auth')
def auth():
	auth = request.authorization
	if auth and (auth.password == USER_PASSWORD):
		
		token = jwt.encode({'user': auth.username}, app.secret_key)
		return jsonify({'token': token.decode('UTF-8')})

	return make_response('Could not verify credentials', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

def token_required(f):
	@wraps(f)
	def decorated(*args,**kwargs):
		token = request.args.get('token')
		
		if('x-access-token' in request.headers):
			token = request.headers['x-access-token']

		if not token:
			return jsonify({'message': miscFunctions.errorCodes(3)})

		try:
			data = jwt.decode(token, app.secret_key)
		except:
			return jsonify({'message': miscFunctions.errorCodes(4)})

		return f(*args,**kwargs)

	return decorated

### Routes

@app.route('/transactions/insert', methods=['POST'])
@token_required
def trs_insert():
	if( request.method == 'POST' ):
		try:
			content = request.get_json()
			print(content,len(content))
			if(len(content) == 1):
				if(fileFormatting.validateFormat(content,'transactions')):
					result = db['transactions'].insert_one(content[0])
					return jsonify({"status": "success", 'inserted_documents': 1})
				else:
					return jsonify({"status": "error", "message": miscFunctions.errorCodes(2)})
			else:
				insert_query = []
				for doc in content:
					insert_query.append(fileFormatting.validateFormat(content, 'transactions'))
				result = db['transactions'].insert_many(content)
				return jsonify({'status': 'success', 'inserted_documents': insert_query.count(True)})

						
		except Exception as e:
			print(str(e))
			return jsonify({"status": "error", "message": miscFunctions.errorCodes(1)})

@app.route('/transactions/get', methods=['GET'])
@token_required
def trs_get():
	if( request.method == 'GET'):
		try:
			data = db['transactions'].find()
			return jsonify(miscFunctions.vectorize(data))
		except:
			return jsonify({"status": "error", "message": miscFunctions.errorCodes(1)})

@app.route('/transactions/patch', methods=['PATCH'])
@token_required
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
@token_required
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
@token_required
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

