from flask import Flask, jsonify, request
from flask_cors import CORS

from datetime import datetime

from utils import *
from firebase_utils import *

app = Flask(__name__)

app.config.from_object(__name__)

CORS(app, resources={r"/*":{'origins':"*"}})

@app.route('/api/add/record', methods=['POST'])
def add_record_route():
    data = request.get_json()

    user_id = data['userId']
    records = data['records']

    for record in records:
        add_record(user_id, record)

    return jsonify({'status': 'success'}), 200

@app.route('/api/update/record/<user_id>/<record_id>', methods=['PUT'])
def update_record_route(user_id, record_id):
    data = request.json
    record = data['record']
    update_record(user_id, record_id, record)
    return jsonify({'status': 'success'}), 200

@app.route('/api/get/record/<user_id>/<record_id>', methods=['GET'])
def get_record_route(user_id, record_id):
    record = get_record(user_id, record_id)
    if record:
        return jsonify({'status': 'success', 'record': record}), 200
    else:
        return jsonify({'status': 'not found'}), 404

@app.route('/api/get/records/<user_id>/<date>', methods=['GET'])
def get_records_route(user_id, date):
    try:
        records = get_all_records_by_date(user_id, date)
        return jsonify({'status': 'success', 'records': records}), 200
    except Exception as e:
        return jsonify({'status': 'failure', 'message': str(e)}), 400

@app.route('/api/get/record', methods=['GET'])
def get_record_by_rid():
    rid = request.args.get('rid')

#     print(rid)

#     if not rid:
#         return jsonify({"error": "Record ID is required"}), 400

#     # fetch data from database with rid

#     record = {
#         "rid": "001",
#         "date": "2024-05-19",
#         "name" : "cake",
#         "amount": 360,
#         "tags": ["Food", "Gift", "i don't know"],
#         "type": "expense"
#     }
    
#     return jsonify(record)

# @app.route('/api/get/all_records', methods=['GET'])
# def get_all_records():
#     # fetch data from database

#     records = [
#         {
#           "rid": "001",
#           "date": "2024-05-19",
#           "name": "cake",
#           "amount": 360,
#           "tags": ["Food", "Gift", "i don't know"],
#           "type": "expense",
#         },
#         {
#           "rid": "002",
#           "date": "2024-05-20",
#           "name": "dinner",
#           "amount": 100,
#           "tags": ["Food"],
#           "type": "expense",
#         },
#         {
#           "rid": "003",
#           "date": "2024-05-21",
#           "name": "t-shirt",
#           "amount": 399,
#           "tags": ["Clothing"],
#           "type": "income",
#         },
#       ]
    
#     return jsonify(records)

@app.route('/api/get/stock_info', methods=['GET'])
def get_stock_info_by_id_route():
    stock_id = request.args.get('stock_id', default='2330', type=str)

    result = get_stock_info_by_id(stock_id)

    return jsonify(result)

@app.route('/api/get/stock_data', methods=['GET'])
def get_stock_data_by_id_route():
    stock_id = request.args.get('stock_id', default='2330', type=str)
    timescale = request.args.get('timescale', default='1D', type=str)

    result = get_stock_data_by_id(stock_id, timescale)

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
