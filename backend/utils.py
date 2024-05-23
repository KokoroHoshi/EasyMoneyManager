import yfinance as yf
from datetime import datetime, timedelta

def check_stock_exist(symbol):
    stock = yf.Ticker(symbol)
    return 'symbol' in stock.info

def get_stock_by_id(stock_id, timescale):
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
        data = stock.history(start=current_time.strftime('%Y-%m-%d'), interval='5m')
    elif timescale == '1W':
        start_time = current_time - timedelta(weeks=1)
        data = stock.history(start=start_time.strftime('%Y-%m-%d'), end=(current_time + timedelta(weeks=1)).strftime('%Y-%m-%d'), interval='1h')    
    elif timescale == '1M':
        start_time = current_time - timedelta(days=30)
        data = stock.history(start=start_time.strftime('%Y-%m-%d'), end=(current_time + timedelta(weeks=1)).strftime('%Y-%m-%d'), interval='1d')    
    elif timescale == '1Y':
        start_time = current_time - timedelta(days=365)
        data = stock.history(start=start_time.strftime('%Y-%m-%d'), end=(current_time + timedelta(weeks=1)).strftime('%Y-%m-%d'), interval='5d')
    else:
        raise ValueError("Invalid timescale")


    data = data.to_dict(orient='index')
    data = {
        timestamp.to_pydatetime().strftime('%Y-%m-%d %H:%M:%S'): values for timestamp, values in data.items()
    }
  
    return data