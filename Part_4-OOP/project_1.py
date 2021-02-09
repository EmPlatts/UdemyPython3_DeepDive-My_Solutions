# PROJECT 1
# Note: rough

import numbers
import itertools
from datetime import timedelta, datetime
from collections import namedtuple

Confirmation = namedtuple('Confirmation', 'account_number, transaction_code, transaction_id, time_utc, time')

class TimeZone:
    def __init__(self, name, offset_hours, offset_minutes):
        if name is None or len(str(name).strip())==0:
            raise ValueError("Timezone name required.")
        
        self._name = str(name).strip()
        
        if not isinstance(offset_hours, numbers.Integral):
            raise ValueError("Hours offset must be an interger.")

        if not isinstance(offset_minutes, numbers.Integral):
            raise ValueError("Minutes offset must be an interger.")

        if offset_minutes < -59 or offset_minutes > 59:
            raise ValueError("Minutes offset must between -59 and 59 (inclusive).")

        offset = timedelta(hours=offset_hours, minutes=offset_minutes)
        if offset < timedelta(hours=-12, minutes=0) or offset > timedelta(hours=14, minutes=0):
            raise ValueError("Offset must be between -12:00 and +14:00 (inclusive).")

        self._offset_hours = offset_hours
        self._offset_minutes = offset_minutes
        self._offset = offset

    @property
    def name(self):
        return self._name

    @property
    def offset(self):
        return self._offset

    def __repr__(self):
        return (f"Timezone(name='{self.name}', "
                f"offset_hours={self._offset_hours}, "
                f"offset_minutes={self._offset_minutes})")

    def __eq__(self, other):
        return (isinstance(other, TimeZone) and 
                self.name==other.name and 
                self._offset_hours==other._offset_hours and 
                self._offset_minutes==other._offset_minutes)


class Account:
    """Basic bank account class.
    """
    _interest_rate = 0.05
    _transaction_codes = {
        'deposit' : 'D',
        'withdraw' : 'W',
        'interest' : 'I',
        'rejected' : 'X'
        }

    transaction_cntr = itertools.count(100)

    def __init__(self, acc_no, first_name, last_name, starting_balance=0, time_zone=None):
        if not isinstance(acc_no, numbers.Integral) or len(str(acc_no)) != 6:
            raise ValueError("Account number must be 6 digits long.")
        
        self.acc_no = acc_no
        self.first_name = Account.validate_name(first_name, 'First name')
        self.last_name = Account.validate_name(last_name, 'Last name')
        
        if time_zone is None:
            time_zone = TimeZone('UTC', 0, 0)

        if not isinstance(time_zone, TimeZone):
            raise ValueError("Time zone must be a valid TimeZone object.")

        self.time_zone = time_zone
        self._balance = Account.validate_real_number(starting_balance, min_value=0)

    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, value):
        self._first_name = Account.validate_name(value, 'First name')

    @property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, value):
        self._last_name = Account.validate_name(value, 'Last name')

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def time_zone(self):
        return self._time_zone

    @time_zone.setter
    def time_zone(self, value):
        if not isinstance(value, TimeZone):
            raise ValueError('Time zone must be a valid TimeZone object.')
        self._time_zone = value

    @property
    def balance(self):
        return self._balance

    @classmethod
    def interest_rate(cls):
        return cls._interest_rate

    # There is a more elegant way to do this but still need to cover class methods
    @classmethod
    def get_interest_rate(cls):
        return cls._interest_rate

    @classmethod
    def set_interest_rate(cls, value):
        if not isinstance(value, numbers.Real):
            raise ValueError('Interest rate must be real number.')
        if value < 0 or value > 1:
            raise ValueError('Interest rate between 0 and 1.')
        cls._interest_rate = value

    @staticmethod
    def validate_name(name, field):
        if name is None or len(str(name).strip())==0:
            raise ValueError(f'{field} must be non-empty string')
        return str(name).strip()

    @staticmethod
    def validate_real_number(value, min_value=None):
        if not isinstance(value, numbers.Real):
            raise ValueError('Value must be a real number.')
        if min_value is not None and value < min_value:
            raise ValueError(f'Value must be at least {min_value}')
        return value

    def generate_conf_code(self, transaction_code):
        dt_str = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        return f'{transaction_code}-{self.acc_no}-{dt_str}-{next(Account.transaction_cntr)}'

    @staticmethod
    def parse_conf_code(conf_code, preferred_time_zone=None):
        # in reality would need checks here to make sure conf_code is valid
        transaction_code, acc_no, dt_utc, transaction_id = conf_code.split('-')
        try:
            formatted_dt_utc = datetime.strptime(dt_utc, '%Y%m%d%H%M%S')
        except ValueError as ex:
            raise ValueError('Invalid transaction datetime') from ex
        if preferred_time_zone is None:
            preferred_time_zone = TimeZone('UTC', 0, 0)
        if not isinstance(preferred_time_zone, TimeZone):
            raise ValueError('Invalid TimeZone specified.')
        dt_preferred = formatted_dt_utc + preferred_time_zone.offset
        dt_preferred_str = f"{dt_preferred.strftime('%Y-%m-%d %H:%M:%S')} ({preferred_time_zone.name})"
        return Confirmation(acc_no, transaction_code, transaction_id, formatted_dt_utc.isoformat(), dt_preferred_str)

    def deposit(self, value):
        value = Account.validate_real_number(value, min_value=0.01)
        transaction_code = Account._transaction_codes['deposit']
        conf_code = self.generate_conf_code(transaction_code)
        self._balance += value
        return conf_code
    
    def withdraw(self, value):
        value = Account.validate_real_number(value, min_value=0.01)
        accepted = False
        if self.balance - value < 0:
            transaction_code = Account._transaction_codes['rejected']
        else:
            transaction_code = Account._transaction_codes['withdraw']
            accepted = True
        conf_code = self.generate_conf_code(transaction_code)

        if accepted:
            self._balance -= value            
        return conf_code

    def pay_interest(self):
        interest = self.balance * Account.get_interest_rate()
        conf_code = self.generate_conf_code(self._transaction_codes['interest'])
        self._balance += interest
        return conf_code


p1 = Account(acc_no=123545, first_name='Chelsea', last_name='Jones', starting_balance=100)
