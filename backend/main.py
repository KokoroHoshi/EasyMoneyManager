from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

app.config.from_object(__name__)

CORS(app, resources={r"/*":{'origins':"*"}})

@app.route('/record', methods=['GET'])
def test():
    return("axios test")

@app.route('/api/stock', methods=['GET'])
def get_stock_data():
    timescale = request.args.get('timescale', '1D')
    # 假設有一個函數來根據時間尺度獲取股票數據
    data = get_stock_data_by_timescale(timescale)
    return jsonify(data)

def get_stock_data_by_timescale(timescale):
    # 模擬數據
    if timescale == '1D':
        return [{'date': '2024-05-01', 'price': 0.1}, {'date': '2024-05-02', 'price': 2}, {'date': '2024-05-03', 'price': 4}]
    elif timescale == '1W':
        return [{'date': '2024-04-25', 'price': 95}, {'date': '2024-05-01', 'price': 100}, {'date': '2024-05-07', 'price': 105}]
    # 依次類推，根據時間尺度返回不同的模擬數據
    # ...
    return []

if __name__ == "__main__":
    app.run(debug=True)
