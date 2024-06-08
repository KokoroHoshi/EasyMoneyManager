import twstock
import yfinance as yf
from datetime import datetime, timedelta

import joblib
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def check_stock_exist(symbol):
    stock = yf.Ticker(symbol)
    return 'symbol' in stock.info

def get_stock_info_by_id(stock_id):
    stock = twstock.realtime.get(stock_id)
    
    if not stock['success']:
        return None
    
    data = get_stock_data_by_id(stock_id, '1D')

    info = {
        'stock_name': stock['info']['fullname'],
        'stock_id': stock['info']['code'],
        'current_price': round(data[list(data)[-1]]['Close'], 2)
    }

    return info

def get_stock_data_by_id(stock_id, timescale):
    # interval
    # 1 2 5 15 30 60 90m
    # 1h
    # 1d 5d
    # 1wk
    # 1 3mo
    found_stock = False
    for suffix in ['.TW', '.TWO']:
        symbol = stock_id + suffix
        if check_stock_exist(symbol):
            stock = yf.Ticker(symbol)
            found_stock = True
            break
    if not found_stock:
        return None

    current_time = datetime.now()

    if timescale == '1D':
        if current_time.weekday() == 5: # Saturday
            start_time = (current_time - timedelta(days=1)).replace(hour=9, minute=0, second=0)
        elif current_time.weekday() == 6: # Sunday
            start_time = (current_time - timedelta(days=2)).replace(hour=9, minute=0, second=0)
        elif current_time.time() < datetime.strptime('09:00:00', '%H:%M:%S').time():
            start_time = (current_time - timedelta(days=1)).replace(hour=9, minute=0, second=0)
        else:
            start_time = current_time

        data = stock.history(start=start_time.strftime('%Y-%m-%d'), interval='5m')
        data = data.to_dict(orient='index')
        data = {
            timestamp.to_pydatetime().strftime('%Y-%m-%d %H:%M'): values for timestamp, values in data.items()
        }
    elif timescale == '1W':
        start_time = current_time - timedelta(weeks=1)
        data = stock.history(start=start_time.strftime('%Y-%m-%d'), end=(current_time + timedelta(weeks=1)).strftime('%Y-%m-%d'), interval='1h')    
        data = data.to_dict(orient='index')
        data = {
            timestamp.to_pydatetime().strftime('%Y-%m-%d %H:%M'): values for timestamp, values in data.items()
        }
    elif timescale == '1M':
        start_time = current_time - timedelta(days=30)
        data = stock.history(start=start_time.strftime('%Y-%m-%d'), end=(current_time + timedelta(weeks=1)).strftime('%Y-%m-%d'), interval='1d')    
        data = data.to_dict(orient='index')
        data = {
            timestamp.to_pydatetime().strftime('%Y-%m-%d'): values for timestamp, values in data.items()
        }
    elif timescale == '1Y':
        start_time = current_time - timedelta(days=365)
        data = stock.history(start=start_time.strftime('%Y-%m-%d'), end=(current_time + timedelta(weeks=1)).strftime('%Y-%m-%d'), interval='5d')
        data = data.to_dict(orient='index')
        data = {
            timestamp.to_pydatetime().strftime('%Y-%m-%d'): values for timestamp, values in data.items()
        }
    else:
        raise ValueError("Invalid timescale")
  
    return data

def get_stock_data_by_id_for_model(stock_id):
    found_stock = False
    for suffix in ['.TW', '.TWO']:
        symbol = stock_id + suffix
        if check_stock_exist(symbol):
            stock = yf.Ticker(symbol)
            found_stock = True
            break
    if not found_stock:
        return None

    current_time = datetime.now()

    start_time = (current_time - timedelta(days=5)).replace(hour=9, minute=0, second=0)

    data = stock.history(start=start_time.strftime('%Y-%m-%d'), interval='1m')

    if data.empty:
        print("No data fetched.")
        return None

    data = data['Close'].tolist()

    # Pad the prices with the last known price to reach 384 points
    if len(data) < 384:
        data = data + [data[-1]] * (384 - len(data))
    else:
        data = data[-384:]

    return data

def load_model(model_path):
    return joblib.load(model_path)

def predict(model, x):
    print(x.shape)
    if len(x) != 384:
        raise ValueError("Input shape must be (384,)")
    y_hat = model.predict([x])  # model.predict expects 2D array
    # print(f"Model raw output: {y_hat}") 
    return y_hat[96:]

def normalize_data(data):
    scaler = MinMaxScaler()
    data = np.array(data).reshape(-1, 1)
    normalized_data = scaler.fit_transform(data)
    return normalized_data.flatten(), scaler

def inverse_transform(predictions, scaler):
    predictions = np.array(predictions).reshape(-1, 1)
    return scaler.inverse_transform(predictions).flatten()

# Usage example
if __name__ == "__main__":
    stock_id = '2330'  # Example stock ID
    model_path = './model/random_forest_stock.pkl'

    data = get_stock_data_by_id_for_model(stock_id)
    if data is None:
        print("Stock data not found.")
    else:
        normalized_data, scaler = normalize_data(data)
        model = load_model(model_path)
        try:
            prediction = predict(model, normalized_data)
            actual_prices = inverse_transform(prediction, scaler)
            print("results: ", actual_prices)
        except ValueError as e:
            print("error: ", e)