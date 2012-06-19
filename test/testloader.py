'''
Created on 13/11/2011

@author: Renzo Nuccitelli
'''
import unittest

if __name__ == '__main__':
    loader=unittest.TestLoader()
    tests=loader.discover(".","*tests.py")
    runner=unittest.TextTestRunner()
    runner.run(tests)
    