""" EXERCISE 3
Do the serialization again, but using Marshmallow.
"""

from datetime import date, datetime
from decimal import Decimal
from marshmallow import Schema, fields, post_load

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


# Marshmallow Schemas
class StockSchema(Schema):
    symbol = fields.Str()
    date = fields.Date()
    open = fields.Decimal(as_string=True)
    high = fields.Decimal(as_string=True)
    low = fields.Decimal(as_string=True)
    close = fields.Decimal(as_string=True)
    volume = fields.Integer()

    @post_load
    def make_stock(self, data, **kwargs):
        data['open_'] = data.pop('open')
        data['date_'] = data.pop('date')
        return Stock(**data)


class TradeSchema(Schema):
    symbol = fields.Str()
    timestamp = fields.DateTime()
    order = fields.Str()
    price = fields.Decimal(as_string=True)
    volume = fields.Integer()
    commission = fields.Decimal(as_string=True)

    @post_load
    def make_trade(self, data, **kwargs):
        return Trade(**data)


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

class MarketSchema(Schema):
    trades = fields.Nested(TradeSchema, many=True)
    quotes = fields.Nested(StockSchema, many=True)


stock_schema = StockSchema()
trade_schema = TradeSchema()
market_schema = MarketSchema()

activity_serialised = market_schema.dumps(activity)

activity_deserialised = MarketSchema().loads(activity_serialised)

print(activity_deserialised)
print(activity==activity_deserialised)