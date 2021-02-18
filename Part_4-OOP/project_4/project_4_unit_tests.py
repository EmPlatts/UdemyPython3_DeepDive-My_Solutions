# Unit tests using unittest as per Fred

from project_4_part_2 import IntegerField, CharField

import numbers
import unittest

class TestIntegerField(unittest.TestCase):
    @staticmethod
    def create_test_class(min_, max_):
        obj = type('TestClass', (), {'age': IntegerField(min_, max_)})
        return obj()
    
    def test_set_age_okay(self):
        """Tests valid values can be assigned/retrieved"""
        min_ = 5
        max_ = 10
        obj = self.create_test_class(min_, max_)
        valid_values = range(min_, max_)

        for i, value in enumerate(valid_values):
            with self.subTest(test_number=i):
                obj.age = value
                self.assertEqual(value, obj.age)

    def test_set_age_invalid(self):
        """Test that invalid values raise ValueErrors"""
        min_ = -10
        max_ = 10
        obj = self.create_test_class(min_, max_)
        bad_values = list(range(min_-5, min_))
        bad_values += list(range(max_+1, max_+5))
        bad_values += [10.5, 1+0j, 'abc', (1, 2)]

        for i, value in enumerate(bad_values):
            with self.subTest(test_number=i):
                with self.assertRaises(ValueError):
                    obj.age = value
    
    def test_min_age_only(self):
        """Tests that one can specify min value only"""
        min_ = 0
        max_ = None
        obj = self.create_test_class(min_, max_)
        values = range(min_, min_+100, 10)

        for i, value in enumerate(values):
            with self.subTest(test_number=i):
                obj.age = value
                self.assertEqual(value, obj.age)

    def test_max_age_only(self):
        """Tests that one can specify max value only"""
        min_ = None
        max_ = 10
        obj = self.create_test_class(min_, max_)
        values = range(max_-100, max_, 10)

        for i, value in enumerate(values):
            with self.subTest(test_number=i):
                obj.age = value
                self.assertEqual(value, obj.age)
    
    def test_max_age_no_limits(self):
        """Tests that one doesn't need to set limits"""
        min_ = None
        max_ = None
        obj = self.create_test_class(min_, max_)
        values = range(-100, 100, 10)

        for i, value in enumerate(values):
            with self.subTest(test_number=i):
                obj.age = value
                self.assertEqual(value, obj.age)

class TestCharField(unittest.TestCase):
    @staticmethod
    def create_test_class(min_, max_):
        obj = type('TestClass', (), {'name': CharField(min_, max_)})
        return obj()
    
    def test_set_name_okay(self):
        """Tests valid values can be assigned/retrieved"""
        min_ = 1
        max_ = 10
        obj = self.create_test_class(min_, max_)
        valid_values = ['a', 'abc', 'abcdefg']

        for i, value in enumerate(valid_values):
            with self.subTest(test_number=i):
                obj.name = value
                self.assertEqual(value, obj.name)

    def test_set_name_invalid(self):
        """Test that invalid values raise ValueErrors"""
        min_ = 1
        max_ = 5
        obj = self.create_test_class(min_, max_)
        bad_values = ['', 'abcdef', 3, str(100000)]

        for i, value in enumerate(bad_values):
            with self.subTest(test_number=i):
                with self.assertRaises(ValueError):
                    obj.name = value
    
    def test_set_name_min_only(self):
        """Tests that one can specify min value only"""
        min_ = 1
        max_ = None
        obj = self.create_test_class(min_, max_)
        valid_lengths = range(min_, min_+100, 10)
        for i, length in enumerate(valid_lengths):
            value = 'a'*length
            with self.subTest(test_number=i):
                obj.name = value
                self.assertEqual(value, obj.name)

    def test_set_name_max_only(self):
        """Tests that we can specify a max length only"""
        min_ = None
        max_ = 10
        obj = self.create_test_class(min_, max_)
        valid_lengths = range(max_-100, max_, 10)
        for i, length in enumerate(valid_lengths):
            value = 'a'*length
            with self.subTest(test_number=i):
                obj.name = value
                self.assertEqual(value, obj.name)

    def test_set_name_min_negative_or_none(self):
        """Tests that setting a negative or None length results in a zero length"""
        obj = self.create_test_class(-10, 100)
        self.assertEqual(type(obj).name._min, 0)
        self.assertEqual(type(obj).name._max, 100)
        
        obj = self.create_test_class(None, None)
        self.assertEqual(type(obj).name._min, 0)
        self.assertIsNone(type(obj).name._max)

    def test_set_name_no_limits(self):
        """Tests that we can use CharField without any limits"""
        min_ = None
        max_ = None
        obj = self.create_test_class(min_, max_)
        valid_lengths = range(0, 100, 10)
        for i, length in enumerate(valid_lengths):
            value = 'a'*length
            with self.subTest(test_number=i):
                obj.name = value
                self.assertEqual(value, obj.name)
    
def run_tests(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

run_tests(TestIntegerField)
run_tests(TestCharField)