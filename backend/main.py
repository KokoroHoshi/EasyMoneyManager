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

@app.route('/api/get/record', methods=['GET'])
def get_record_route():
    user_id = request.args.get('user_id')
    record_id = request.args.get('record_id')

    if not user_id or not record_id:
        return jsonify({'status': 'error', 'message': 'Missing user_id or record_id'}), 400

    record = get_record(user_id, record_id)
    if record:
        return jsonify({'status': 'success', 'record': record}), 200
    else:
        return jsonify({'status': 'not found'}), 404

@app.route('/api/get/records/<user_id>/<date>', methods=['GET'])
def get_records_route(user_id, date):
    try:
        records = get_records_by_date(user_id, date)
        return jsonify({'status': 'success', 'records': records}), 200
    except Exception as e:
        return jsonify({'status': 'failure', 'message': str(e)}), 400

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
