# Many, many more one could do

from project_2 import Mod
import unittest

def run_tests(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

class TestMod(unittest.TestCase):
    def test_valid(self):
        with self.assertRaises(ValueError):
            mod_1 = Mod(2,-3)
            mod_2 = Mod(0.5,2)
            mod_3 = Mod(2,0)

    def test_equal_Mod_int(self):
        self.assertEqual(Mod(3,2), 1)
        self.assertEqual(Mod(12,1), 12)
        self.assertEqual(Mod(-5,2), 1)
    
    def test_equal_Mod_Mod(self):
        self.assertEqual(Mod(3,2), Mod(7,2))
        self.assertEqual(Mod(2,13), Mod(28,13))
        self.assertEqual(Mod(1,2), Mod(-5,2))
    
    def test_lt(self):
        self.assertLess(Mod(1,3), Mod(2,3))
        self.assertLess(Mod(-55,23), 15)

run_tests(TestMod)

