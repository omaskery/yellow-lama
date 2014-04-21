#!/usr/bin/python

import unittest

#
# This example involves writing a simple 'comparison' function
#
# The input will be two integers, a and b
# If a is greater than b, the output should be "greater"
# If a is less than b, the output should be "lesser"
# If a is equal to b, the output should be "equal"
#

def compare(num_a, num_b):
    output = ""

    # your own code here
    
    return output

class CompareTestCase(unittest.TestCase):
    def test_lesser(self):
        a = 10
        b = 100
        c = compare(a, b)

        self.assertEqual(c, "lesser",
            "expected this comparison to say 'lesser'")
    def test_greater(self):
        a = 42
        b = 10
        c = compare(a, b)

        self.assertEqual(c, "greater",
            "expected this comparison to say 'greater'")
    def test_equal(self):
        a = 30
        b = 30
        c = compare(a, b)

        self.assertEqual(c, "equal",
            "expected this comparison to say 'equal'")

def suite():
    suite = unittest.TestSuite()
    suite.addTest(CompareTestCase('test_lesser'))
    suite.addTest(CompareTestCase('test_greater'))
    suite.addTest(CompareTestCase('test_equal'))
    return suite

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
