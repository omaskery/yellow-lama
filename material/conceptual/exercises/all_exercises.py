#!/usr/bin/python

import unittest
import reverse
import comparison
import bottles

def easy_suite():
    return unittest.TestSuite([
        reverse.suite(),
        comparison.suite()
    ])

def medium_suite():
    return unittest.TestSuite([
        bottles.suite()
    ])

def hard_suite():
    return unittest.TestSuite([
    ])

def whole_suite():
    return unittest.TestSuite([
        easy_suite(),
        medium_suite(),
        hard_suite()
    ])

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(whole_suite())
