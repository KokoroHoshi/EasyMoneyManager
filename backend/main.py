from flask import Flask, jsonify, request
from flask_cors import CORS

from utils import *
from firebase_utils import *

app = Flask(__name__)

app.config.from_object(__name__)

CORS(app, resources={r"/*":{'origins':"*"}})

@app.route('/', methods=['GET'])
def root():
    return jsonify({'status': 'success', 'message': 'HHW!'}), 200

@app.route('/api/add/record', methods=['POST'])
def add_record_route():
    data = request.get_json()

    user_id = data['userId']
    records = data['records']

    if not user_id or not records:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

    for record in records:
        add_record(user_id, record)

    return jsonify({'status': 'success'}), 200

@app.route('/api/get/record', methods=['GET'])
def get_record_route():
    print("Route hit!")  # 確認 route 有被呼叫
    user_id = request.args.get('user_id')
    record_id = request.args.get('record_id')

    print("DEBUG: user_id=", user_id, " record_id=", record_id)  # <--- 加這行

    if not user_id or not record_id:
        return jsonify({'status': 'error', 'message': 'Missing user_id or record_id'}), 400

    record = get_record(user_id, record_id)
    if record:
        return jsonify({'status': 'success', 'record': record}), 200
    else:
        return jsonify({'status': 'not found'}), 404

@app.route('/api/update/record', methods=['PUT'])
def update_record_route():
    data = request.get_json()

    user_id = data.get('userId')
    record_id = data.get('record_id')
    record = data.get('record')

    if not user_id or not record_id or not record:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

    update_record(user_id, record_id, record)

    return jsonify({'status': 'success'}), 200
    
@app.route('/api/delete/record', methods=['DELETE'])
def delete_record_route():
    data = request.get_json()

    user_id = data.get('userId')
    record_id = data.get('record_id')

    if not user_id or not record_id:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

    delete_record(user_id, record_id)

    return jsonify({'status': 'success'}), 200

@app.route('/api/get/records', methods=['GET'])
def get_records_route():
    user_id = request.args.get('user_id')
    start_utc = request.args.get('start')  # ISO 字串
    end_utc = request.args.get('end')      # ISO 字串

    if not user_id or not start_utc or not end_utc:
        return jsonify({'status': 'error', 'message': 'Missing parameters'}), 400

    try:
        # 轉成 datetime
        from datetime import datetime
        start_dt = datetime.fromisoformat(start_utc.replace("Z", "+00:00"))
        end_dt = datetime.fromisoformat(end_utc.replace("Z", "+00:00"))

        # 從資料庫抓 UTC 範圍
        records = get_records_by_utc_range(user_id, start_dt, end_dt)

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

@app.route('/api/get/stock_prediction', methods=['GET'])
def get_stock_prediction_by_id_route():
    stock_id = request.args.get('stock_id', default='2330', type=str)

    result = get_stock_prediction_by_id(stock_id)

    return jsonify(result)

if __name__ == "__main__":
    try:
        init_model()
    except:
        print("Init model failed.")

    # app.run(debug=True)
    app.run()
