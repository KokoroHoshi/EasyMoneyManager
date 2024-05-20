from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

app.config.from_object(__name__)

CORS(app, resources={r"/*":{'origins':"*"}})

@app.route('/record', methods=['GET'])
def test():
    return("axios test")

@app.route('/api/get-stock-data', methods=['GET'])
def get_stock_data():
    stock_data = [
        {
            "date": "2012-04-02",
            "open": 85.9757,
            "high": 90.6657,
            "low": 85.7685,
            "close": 90.5257,
            "volume": 660187068,
        },
        {
            "date": "2012-04-09",
            "open": 89.4471,
            "high": 92,
            "low": 86.2157,
            "close": 86.4614,
            "volume": 912634864,
        }
    ]

    return jsonify(stock_data)

if __name__ == "__main__":
    app.run(debug=True)
