from project_1 import TimeZone, Account
import unittest
from datetime import datetime, timedelta

#there are a whole bunch more tests one could add

def run_tests(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

class TestAccount(unittest.TestCase):

    def setUp(self):
        self.acc_no = 110020
        self.first_name = 'FIRST'
        self.last_name = 'LAST'
        self.balance = 100.00
        self.tz = TimeZone('TZ', 1, 30)

    def create_account(self):
        return Account(self.acc_no, self.first_name, self.last_name, self.balance, self.tz)
   
    def test_create_timezone(self):
        tz = TimeZone('ABC', -1, -30)
        self.assertEqual('ABC', tz.name)
        self.assertEqual(timedelta(hours=-1, minutes=-30), tz.offset)
        
    def test_timezones_equal(self):
        tz1 = TimeZone('ABC', -1, -30)
        tz2 = TimeZone('ABC', -1, -30)
        self.assertEqual(tz1, tz2)
        
    def test_timezones_not_equal(self):
        tz = TimeZone('ABC', -1, -30)
        
        test_timezones = (
            TimeZone('DEF', -1, -30),
            TimeZone('ABC', -1, 0),
            TimeZone('ABC', 1, -30)
        )
        for i, test_tz in enumerate(test_timezones): #see how to do this in pytest 
            with self.subTest(test_name=f'Test #{i}'):
                self.assertNotEqual(tz, test_tz)

    def test_create_account(self):        
        a = self.create_account()

        self.assertEqual(self.acc_no, a.acc_no)
        self.assertEqual(self.first_name, a.first_name)
        self.assertEqual(self.last_name, a.last_name)
        self.assertEqual(self.first_name + ' ' + self.last_name, a.full_name)
        self.assertEqual(self.tz, a.time_zone)
        self.assertEqual(self.balance, a.balance)

    def test_create_account_blank_first_name(self):
        self.first_name = ''
        with self.assertRaises(ValueError):
            a = self.create_account()
        self.first_name = None
        with self.assertRaises(ValueError):
            a = self.create_account()

    def test_create_account_blank_last_name(self):
        self.last_name = ''
        with self.assertRaises(ValueError):
            a = self.create_account()
        self.last_name = None
        with self.assertRaises(ValueError):
            a = self.create_account()

    def test_create_account_negative_balance(self):
        self.balance = -100.00
        with self.assertRaises(ValueError):
            a = self.create_account()

    def test_account_deposit_negative_amount(self):
        deposit_value = -100
        a = self.create_account()
        with self.assertRaises(ValueError):
            conf_code = a.deposit(deposit_value)

    def test_account_withdraw_ok(self):
        withdraw_value = 20
        a = self.create_account()
        conf_code = a.withdraw(withdraw_value)
        self.assertEqual(self.balance-withdraw_value, a.balance)
        self.assertIn('W-', conf_code)

    def test_account_withdraw_overdraw(self):
        withdraw_value = 200
        a = self.create_account()
        conf_code = a.withdraw(withdraw_value)
        self.assertIn('X-', conf_code)
        self.assertEqual(self.balance, a.balance)
    

run_tests(TestAccount)


