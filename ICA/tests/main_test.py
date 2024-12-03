import unittest

class TestSum(unittest.TestCase): 


    def test_sum(self):
        self.assertEqual(sum([1,2,3]), 6, "should equal 6")


if __name__ == 'main_test':
    unittest.main()