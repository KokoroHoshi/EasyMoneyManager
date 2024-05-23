import twstock
from datetime import datetime, timedelta

def get_stock_by_code(stock_id, timescale):
    if timescale == '1D':
        return get_realtime_data(stock_id)
    else:
        now = datetime.now()
        
        if timescale == '1W':
            start_date = now - timedelta(weeks=1)
        elif timescale == '1M':
            start_date = now - timedelta(days=30)
        elif timescale == '1Y':
            start_date = now - timedelta(days=365)
        else:
            raise ValueError("Invalid timescale")

        stock = twstock.Stock(stock_id)
        stock_data = stock.fetch_from(start_date.year, start_date.month)

        data = [
            {
                'date': stock.date[i].strftime('%Y-%m-%d'),
                'open': stock.open[i],
                'close': stock.close[i],
                'high': stock.high[i],
                'low': stock.low[i],
                'volume': stock.capacity[i]
            }
            for i in range(len(stock.date))
            if stock.date[i] >= start_date
        ]

        return aggregate_data(data, timescale)

def get_realtime_data(stock_id):
    realtime_data = twstock.realtime.get(stock_id)
    
    if not realtime_data['success']:
        raise ValueError(f"Failed to fetch real-time data for stock {stock_id}")
    
    info = realtime_data['info']
    timestamp = datetime.strptime(info['time'], '%Y-%m-%d %H:%M:%S')
    
    return [
        {
            'date': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'open': realtime_data['realtime']['open'],
            'close': realtime_data['realtime']['latest_trade_price'],
            'high': realtime_data['realtime']['high'],
            'low': realtime_data['realtime']['low'],
            'volume': realtime_data['realtime']['accumulate_trade_volume']
        }
    ]

def aggregate_data(data, timescale):
    if timescale not in ['1D', '1W', '1M', '1Y']:
        raise ValueError("Invalid timescale")

    def group_data(data, key_func):
        grouped_data = {}
        for record in data:
            key = key_func(record['date'])
            if key not in grouped_data:
                grouped_data[key] = {
                    'open': record['open'],
                    'close': record['close'],
                    'high': record['high'],
                    'low': record['low'],
                    'volume': record['volume']
                }
            else:
                grouped_data[key]['high'] = max(grouped_data[key]['high'], record['high'])
                grouped_data[key]['low'] = min(grouped_data[key]['low'], record['low'])
                grouped_data[key]['close'] = record['close']
                grouped_data[key]['volume'] += record['volume']
        return [
            {
                'date': key,
                'open': val['open'],
                'close': val['close'],
                'high': val['high'],
                'low': val['low'],
                'volume': val['volume']
            }
            for key, val in grouped_data.items()
        ]

    if timescale == '1D':
        return data
    elif timescale == '1W':
        return group_data(data, lambda date: datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%U'))
    elif timescale == '1M':
        return group_data(data, lambda date: datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m'))
    elif timescale == '1Y':
        return group_data(data, lambda date: datetime.strptime(date, '%Y-%m-%d').strftime('%Y'))

    return []

if __name__ == "__main__":
    stock_id = '2330'
    timescale = '1D'
    stock_data = get_stock_by_code(stock_id, timescale)
    for record in stock_data:
        print(record)
