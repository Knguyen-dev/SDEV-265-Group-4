'''
- File for running all unit tests

'''

import unittest

def createTestSuite():
    loader = unittest.TestLoader()
    testSuite = loader.discover("./",pattern="test_*.py")
    return testSuite

if __name__ == "__main__":
    suite = createTestSuite()
    testRunner = unittest.TextTestRunner()
    result = testRunner.run(suite)