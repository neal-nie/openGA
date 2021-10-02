"""
function to execute all tests found in the test directory
"""
# Copyright (c) 2015-2021 Neal Nie. All rights reserved.

from pathlib import Path
import sys
import unittest
import xmlrunner


def main():
    tests = unittest.TestLoader().discover("test", "test_*.py")
    testResult = xmlrunner.XMLTestRunner(
        output=str(Path(".").resolve() / "test-reports")
    ).run(tests)

    return not testResult.wasSuccessful()


if __name__ == "__main__":
    sys.exit(main())
