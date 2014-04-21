#!/usr/bin/python

import unittest

#
# This example requires you to reverse the input text
#
# The input variable 'text' will contain a string like
#   "hello"
#
# The output should be the reverse:
#   "olleh"
#

def reverse(text):
    output = ""
    
    # put your own code here
    
    return output

class ReverseTextTest(unittest.TestCase):
    def test_reverse(self):
        test_input = "this is some input"
        expected_output = "tupni emos si siht"

        test_output = reverse(test_input)
        self.assertEqual(test_output, expected_output,
            "the test output was not the reverse of the test input!")

def suite():
    suite = unittest.TestSuite()
    suite.addTest(ReverseTextTest('test_reverse'))
    return suite

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
