from flask import Flask, jsonify, request
from flask_cors import CORS

from datetime import datetime

from utils import *

app = Flask(__name__)

app.config.from_object(__name__)

CORS(app, resources={r"/*":{'origins':"*"}})

@app.route('/api/get/record', methods=['GET'])
def get_record_by_rid():
    rid = request.args.get('rid')

    print(rid)

    if not rid:
        return jsonify({"error": "Record ID is required"}), 400

    # fetch data from database with rid

    record = {
        "rid": "001",
        "date": "2024-05-19",
        "name" : "cake",
        "amount": 360,
        "tags": ["Food", "Gift", "i don't know"],
        "type": "expense"
    }
    
    return jsonify(record)

@app.route('/api/get/all_records', methods=['GET'])
def get_all_records():
    # fetch data from database

    records = [
        {
          "rid": "001",
          "date": "2024-05-19",
          "name": "cake",
          "amount": 360,
          "tags": ["Food", "Gift", "i don't know"],
          "type": "expense",
        },
        {
          "rid": "002",
          "date": "2024-05-20",
          "name": "dinner",
          "amount": 100,
          "tags": ["Food"],
          "type": "expense",
        },
        {
          "rid": "003",
          "date": "2024-05-21",
          "name": "t-shirt",
          "amount": 399,
          "tags": ["Clothing"],
          "type": "income",
        },
      ]
    
    return jsonify(records)

@app.route('/api/post/record', methods=['POST'])
def add_record():
    datetime_format = '%Y-%m-%dT%H:%M:%S.%fZ'

    data = request.get_json()
    name = data['name']
    amount = data['amount']
    tags = ','.join(data['tags'])
    date = datetime.strptime(data['date'], datetime_format)
    type = data['type']
    
    print(data)

    # something like
    # new_record = Record(name=name, amount=amount, tags=tags, date=date, type=type)
    # db.session.add(new_record)
    # db.session.commit()

    return jsonify({'message': 'Record added successfully'})

@app.route('/api/get/stock', methods=['GET'])
def get_stock_by_code_route():
    stock_id = request.args.get('stock_id', default='2330', type=str)
    timescale = request.args.get('timescale', default='1D', type=str)

    result = get_stock_by_id(stock_id, timescale)

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
