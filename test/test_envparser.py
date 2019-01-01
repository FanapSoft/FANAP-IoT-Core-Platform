import unittest  # noqa
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from app import envparser  # noqa


class CheckEnvParser(unittest.TestCase):

    def test_basic(self):
        os.environ['__TEST_INT__'] = '345'
        os.environ['__TEST_STR__'] = 'TEST_VAL'

        ret = envparser.build([
            ('__Hello__', 12, 'int'),
            ('__Kalam__', False, 'bool'),
            ('__TEST_INT__', 249, 'int'),
            ('__TEST_STR__', 'new_value', 'str'),
        ])

        self.assertDictEqual(ret, dict(
            __Hello__=12,
            __Kalam__=False,
            __TEST_INT__=345,
            __TEST_STR__='TEST_VAL'
        ))


if __name__ == '__main__':
    unittest.main()
