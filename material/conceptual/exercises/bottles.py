#!/usr/bin/python

import unittest

#
# This example requires you to output the "99 bottles" song
# (we'll be doing a shortened, 5 bottles of beer version)
#
# The output should be:
#
#   5 bottles of beer on the wall, 5 bottles of beer,
#   take one down, pass it around,
#   4 more bottles of beer on the wall!
#   4 bottles of beer on the wall, 4 bottles of beer,
#   take one down, pass it around,
#   3 more bottles of beer on the wall!
#   3 bottles of beer on the wall, 3 bottles of beer,
#   take one down, pass it around,
#   2 more bottles of beer on the wall!
#   2 bottles of beer on the wall, 2 bottles of beer,
#   take one down, pass it around,
#   1 more bottle of beer on the wall!
#   1 bottle of beer on the wall, 1 bottle of beer,
#   take one down, pass it around,
#   no more bottles of beer on the wall!
#
# Yes, it is technically possible to just copy the test suite
# text into the bottles function, but you don't get anything for
# completing this test except experience, so why bother!
#

def bottles():
    output = ""
    
    # put your own code here
    
    return output

class BottlesTextTest(unittest.TestCase):
    def test_song(self):
        self.maxDiff = None
        self.assertEqual(bottles().strip(),
"""
5 bottles of beer on the wall, 5 bottles of beer,
take one down, pass it around,
4 more bottles of beer on the wall!
4 bottles of beer on the wall, 4 bottles of beer,
take one down, pass it around,
3 more bottles of beer on the wall!
3 bottles of beer on the wall, 3 bottles of beer,
take one down, pass it around,
2 more bottles of beer on the wall!
2 bottles of beer on the wall, 2 bottles of beer,
take one down, pass it around,
1 more bottle of beer on the wall!
1 bottle of beer on the wall, 1 bottle of beer,
take one down, pass it around,
no more bottles of beer on the wall!
""".strip())

def suite():
    suite = unittest.TestSuite()
    suite.addTest(BottlesTextTest('test_song'))
    return suite

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
