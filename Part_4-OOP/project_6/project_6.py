"""PROJECT 6: Exceptions
Suppose we have a Widget online sales application and we are writing the
backend for it. We want a base WidgetException class that we will use as the
base class for all our custom exceptions we raise from our Widget application.

Furthermore we have determined that we will need the following categories of
exceptions:

1. Supplier exceptions
    a. Not manufactured anymore
    b. Production delayed
    c. Shipping delayed

2. Checkout exceptions
    a. Inventory type exceptions
        - out of stock
    b. Pricing exceptions
        - invalid coupon code
        - cannot stack coupons

Write an exception class hierarchy to capture this. In addition, we would like
to implement the following functionality:

    * implement separate internal error message and user error message
    * implement an http status code associated to each exception type (keep it
      simple, use a 500 (server error) error for everything except invalid 
      coupon code, and cannot stack coupons, these can be 400 (bad request)
    * implement a logging function that can be called to log the exception
      details, time it occurred, etc.
    * implement a function that can be called to produce a json string
      containing the exception details you want to display to your user
      (include http status code (e.g. 400), the user error message, etc)
"""
import json
from http import HTTPStatus
from datetime import datetime
import traceback

class WidgetException(Exception):
    http_status = HTTPStatus.INTERNAL_SERVER_ERROR
    internal_err_msg = 'Application exception occured.'

    def __init__(self, *args, user_err_msg=None):
        super().__init__(*args)
        if args:
            self.internal_err_msg = args[0]
        self.user_err_msg = user_err_msg if user_err_msg is not None else self.internal_err_msg

    @property
    def traceback(self):
        return traceback.TracebackException.from_exception(self).format()

    def to_json(self):
        err_object = {
            'status' : self.http_status.value,
            'message' : f'{self.http_status.phrase} : {self.user_err_msg}',
            'category' : type(self).__name__,
            'time_utc' : datetime.utcnow().isoformat()
        }
        return json.dumps(err_object)
    
    def log_exception(self):
        exception = {
            'type' : type(self).__name__,
            'http_status' : self.http_status.value,
            'message' : self.args[0] if self.args else self.internal_err_msg,
            'args' : self.args[1:],
            'time_utc' : datetime.utcnow().isoformat()
        }
        print(f'EXCEPTION: {datetime.utcnow().isoformat()} : {exception}')


class SupplierException(WidgetException):
    internal_err_msg = 'Supplier exception occured.'
    http_status = HTTPStatus.INTERNAL_SERVER_ERROR
    
class NotManufacturedException(SupplierException):
    internal_err_msg = 'Exception occured - no longer manufactured.'
    user_err_msg = 'Unfortunately this product is no longer available.'
    http_status = HTTPStatus.INTERNAL_SERVER_ERROR

class ProductionDelayedException(SupplierException):
    internal_err_msg = 'Exception occured - production is delayed.'
    user_err_msg = "We're sorry, the production of this product is currently delayed."
    http_status = HTTPStatus.INTERNAL_SERVER_ERROR

class ShippingDelayedException(SupplierException):
    internal_err_msg = 'Exception occured - shipping is delayed.'
    user_err_msg = "Please note shipping is currently delayed."
    http_status = HTTPStatus.INTERNAL_SERVER_ERROR

class CheckoutException(WidgetException):
    internal_err_msg = 'Checkout exception occured.'
    http_status = HTTPStatus.INTERNAL_SERVER_ERROR

class InventoryException(CheckoutException):
    internal_err_msg = 'Inventory exception occured.'
    http_status = HTTPStatus.INTERNAL_SERVER_ERROR

class OutOfStockException(InventoryException):
    internal_err_msg = 'Product out of stock.'
    http_status = HTTPStatus.INTERNAL_SERVER_ERROR

class PricingException(CheckoutException):
    internal_err_msg = 'Pricing exception occured during checkout.'
    http_status = HTTPStatus.INTERNAL_SERVER_ERROR

class InvalidCouponCodeException(PricingException):
    internal_err_msg = 'Invalid coupon code.'
    http_status = HTTPStatus.BAD_REQUEST

class CannotStackCouponException(PricingException):
    internal_err_msg = 'Cannot use multiple coupon codes.'
    http_status = HTTPStatus.BAD_REQUEST


# Trying it out
try:
    a = 1 / 0
except ZeroDivisionError:
    try:
        raise WidgetException()
    except WidgetException as ex:
        print(''.join(ex.traceback))

try:
    raise ValueError
except ValueError:
    try:
        raise InvalidCouponCodeException(
            'User tried to use an old coupon', user_err_msg='Sorry, coupon has expired.'
        )
    except InvalidCouponCodeException as ex:
        ex.log_exception()
        print('------------')
        print(ex.to_json())
        print('------------')
        print(''.join(ex.traceback))