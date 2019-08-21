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

@app.route('/transactions', methods=['GET', 'POST'])
def transaction():
	if( request.method == 'POST' ):
		try:
			content = request.get_json()
			if(fileFormatting.validateFormat(content,'transactions')):
				post_id = db['transactions'].insert_one(content).inserted_id
				return jsonify({"status": "success"})
			else:
				return jsonify({"error": miscFunctions.errorCodes(2)})
			
		except Exception as e:
			return str(e)
			#return jsonify({"error": miscFunctions.errorCodes(1)})

@app.route('/')
def index():
	return 'Welcome, its working!'

# Running

if __name__ == '__main__':
    app.secret_key='hiddenpass'
    app.run(debug=True)

