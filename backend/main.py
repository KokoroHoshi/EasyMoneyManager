from flask import Flask, jsonify, request
from flask_cors import CORS

from datetime import datetime

app = Flask(__name__)

app.config.from_object(__name__)

CORS(app, resources={r"/*":{'origins':"*"}})

@app.route('/api/get/record', methods=['GET'])
def get_record():
    rid = request.args.get('rid')

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

@app.route('/api/post/record', methods=['POST'])
def add_record():
    datetime_format = '%Y-%m-%dT%H:%M:%S.%fZ'

    data = request.get_json()
    name = data['name']
    amount = data['amount']
    tags = ','.join(data['tags'])
    date = datetime.strptime(data['date'], datetime_format)
    type = data['type']
    
    print(date)

    # something like
    # new_record = Record(name=name, amount=amount, tags=tags, date=date, type=type)
    # db.session.add(new_record)
    # db.session.commit()

    return jsonify({'message': 'Record added successfully'})

def get_stock_data_by_timescale(timescale):
    # test
    if timescale == '1D':
        return [{'date': '2024-05-01', 'price': 0.1}, {'date': '2024-05-02', 'price': 2}, {'date': '2024-05-03', 'price': 4}]
    elif timescale == '1W':
        return [{'date': '2024-04-25', 'price': 95}, {'date': '2024-05-01', 'price': 100}, {'date': '2024-05-07', 'price': 105}]
    return []

@app.route('/api/get/stock', methods=['GET'])
def get_stock_data():
    # escape later
    timescale = request.args.get('timescale', '1D')
    data = get_stock_data_by_timescale(timescale)
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
