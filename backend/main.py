from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

app.config.from_object(__name__)

CORS(app, resources={r"/*":{'origins':"*"}})

@app.route('/record', methods=['GET'])
def test():
    return("axios test")

@app.route('/api/stock-data', methods=['GET'])
def get_stock_data():
    stock_data = [
        [1537795800000, 55.2],
        [1537882200000, 55.55],
        [1537968600000, 55.1],
        [1538055000000, 56.24],
        [1538141400000, 56.44],
        [1538400600000, 56.81],
        [1538487000000, 57.32],
        [1538573400000, 58.02],
        [1538659800000, 57]
    ]
    return jsonify(stock_data)

if __name__ == "__main__":
    app.run(debug=True)
