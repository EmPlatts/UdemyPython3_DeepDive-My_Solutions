""" EXERCISE 1 and 2

class Stock:
    def __init__(self, symbol, date, open_, high, low, close, volume):
        self.symbol = symbol
        self.date = date
        self.open = open_
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        
class Trade:
    def __init__(self, symbol, timestamp, order, price, volume, commission):
        self.symbol = symbol
        self.timestamp = timestamp
        self.order = order
        self.price = price
        self.commission = commission
        self.volume = volume

Given the above classes write a custom JSONEncoder class to serialize
dictionaries that contain instances of these particular classes. Keep in mind
that you will want to deserialize the data too - so you will need some
technique to indicate the object type in your serialization.

HINT: You can modify the given classes.

Now write code to reverse the serialization you just created. Write a custom
decoder that can deserialize a JSON structure containing Stock and Trade objects.
"""

from datetime import date, datetime
from decimal import Decimal
import json
import re

class Stock:
    def __init__(self, symbol, date_, open_, high, low, close, volume):
        self.symbol = symbol
        self.date = date_
        self.open = open_
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
    
    def __repr__(self):
        return f'Stock(symbol={self.symbol},\n\
                date={self.date},\n\
                open={self.open},\n\
                high={self.high},\n\
                low={self.low},\n\
                close={self.close},\n\
                volume={self.volume})'

    def as_dict(self):
        return dict(symbol=self.symbol,
                    date=self.date,
                    open=self.open,
                    high=self.high,
                    low=self.low,
                    close=self.close,
                    volume=self.volume)

    def __eq__(self, other):
        return isinstance(other,Stock) and self.as_dict()==other.as_dict()


        
class Trade:
    def __init__(self, symbol, timestamp, order, price, volume, commission):
        self.symbol = symbol
        self.timestamp = timestamp
        self.order = order
        self.price = price
        self.volume = volume
        self.commission = commission

    def __repr__(self):
        return f'Trade(symbol={self.symbol},\n\
            timestamp={self.timestamp},\n\
            order={self.order},\n\
            price={self.price},\n\
            commission={self.commission},\n\
            volume={self.volume})'

    def as_dict(self):
        return dict(symbol=self.symbol,
                    timestamp=self.timestamp,
                    order=self.order,
                    price=self.price,
                    volume=self.volume,
                    commission=self.commission)

    def __eq__(self, other):
        return isinstance(other,Trade) and self.as_dict()==other.as_dict()
    

# Encoding
class CustomEncoder(json.JSONEncoder):
    def default(self, arg):
        if isinstance(arg, Stock) or isinstance(arg, Trade):
            result = arg.as_dict()
            result['object'] = arg.__class__.__name__
            return result
        elif isinstance(arg, date) or isinstance(arg, datetime):
            return arg.isoformat()
        elif isinstance(arg, Decimal):
            return str(arg)
        else:
            return super().default(arg)


# Decoding
class CustomDecoder(json.JSONDecoder):
    def decode(self, arg):
        obj = json.loads(arg)
        return self.decode_data(obj)
    
    def _decode_stock(self, obj):
        stock = Stock(obj['symbol'],
                    datetime.strptime(obj['date'], '%Y-%m-%d').date(),
                    Decimal(obj['open']),
                    Decimal(obj['high']),
                    Decimal(obj['low']),
                    Decimal(obj['close']),
                    int(obj['volume']))
        return stock

    def _decode_trade(self, obj):
        trade = Trade(obj['symbol'],
                    datetime.strptime(obj['timestamp'], '%Y-%m-%dT%H:%M:%S'),
                    obj['order'],
                    Decimal(obj['price']),
                    int(obj['volume']),
                    Decimal(obj['commission']))
        return trade

    def _get_type(self, obj):
        if obj.get("object", None)=="Stock":
            return self._decode_stock(obj)
        elif obj.get("object", None)=="Trade":
            return self._decode_trade(obj)
        return obj


    def decode_data(self,obj):
        if isinstance(obj, dict):
            obj = self._get_type(obj)
            if isinstance(obj, dict):
                for key, value in obj.items():
                    obj[key] = self.decode_data(value)
        elif isinstance(obj, list):
            for idx, value in enumerate(obj):
                obj[idx] = self.decode_data(value)
        return obj
    

# Input
activity = {
    "quotes": [
        Stock('TSLA', date(2018, 11, 22), 
              Decimal('338.19'), Decimal('338.64'), Decimal('337.60'), Decimal('338.19'), 365_607),
        Stock('AAPL', date(2018, 11, 22), 
              Decimal('176.66'), Decimal('177.25'), Decimal('176.64'), Decimal('176.78'), 3_699_184),
        Stock('MSFT', date(2018, 11, 22), 
              Decimal('103.25'), Decimal('103.48'), Decimal('103.07'), Decimal('103.11'), 4_493_689)
    ],
    
    "trades": [
        Trade('TSLA', datetime(2018, 11, 22, 10, 5, 12), 'buy', Decimal('338.25'), 100, Decimal('9.99')),
        Trade('AAPL', datetime(2018, 11, 22, 10, 30, 5), 'sell', Decimal('177.01'), 20, Decimal('9.99'))
    ]
}


encoded = json.dumps(activity, cls=CustomEncoder, indent=2)
# print(encoded)

decoded = json.loads(encoded, cls=CustomDecoder)
# print(decoded)

print(activity==decoded)