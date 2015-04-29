import unittest

from tfx import confparse, errors


full_conf = {
    'mysql': {
        'host': 'somehost',
        'user': 'someuser',
        'passwd': 'somepass',
        'db': 'somedb',
    },
    'attribute': 'someattribute',
    'labels': {
        'first': 1,
        'second': 2,
    },
    'limit': 100,
    'ignore_start': 0,
    'ignore_number': 40,
    'features': {
        'enabled': {
            'ktopwords': {
                'k': 20,
            },
            'naivebayes': {
                'threshold': 99.9,
            },
            'anotherfeature': {},
        },
        'default_params': {
            'features_file': 'somefile.json',
            'k': 10,
        },
    },
    'output_file': 'somefile.json',
}


class SanityCheck(unittest.TestCase):
    """
    Make sure that the full_conf is valid
    """
    def runTest(self):
        self.assertTrue(confparse.ConfParser().parse(full_conf))


class _ConfParserTest(unittest.TestCase):
    """
    Defines a basic base test class for testing attributes.
    Only does single-attribute tests (no combinations).
    """
    def setUp(self):
        self.conf = dict(full_conf)
        parser = confparse.ConfParser()
        parser.filename = 'test.json'
        self.parse = parser.parse

    def test_deletion(self):
        del self.conf[self.key]
        self.assertError()

    def test_valid_values(self):
        for valid in self.valid:
            self.conf[self.key] = valid
            self.assertFine()

    def test_invalid_values(self):
        for invalid in self.invalid:
            self.conf[self.key] = invalid
            self.assertError()

    def assertFine(self):
        self.assertTrue(self.parse(self.conf))

    def assertError(self):
        """
        Convenience function, to assert that it raises ConfFileError.
        """
        self.assertRaises(errors.ConfFileError, self.parse, self.conf)


class _OptionalConfParserTest(_ConfParserTest):
    """
    Base class for testing optional keys.
    """
    def test_deletion(self):
        del self.conf[self.key]
        self.assertFine()



class MySQLKeyTest(_ConfParserTest):
    key = 'mysql'
    valid = []
    invalid = [
        {},
        {'host': 'somehost'},
        {'host': 'somehost', 'user': 'someuser'},
    ]


class AttributeKeyTest(_ConfParserTest):
    key = 'attribute'
    valid = [
        'gender',
        'politics',
    ]
    invalid = [
        '',
        [],
        1,
    ]


class LabelsKeyTest(_ConfParserTest):
    key = 'labels'
    valid = [
        {'somelabel': 0, 'anotherlabel': 1,}
    ]
    invalid = [
        [],
        ['somelabel', 'anotherlabel'],
        {'somelabel': '1', 'anotherlabel': '2'},
    ]


class LimitKeyTest(_ConfParserTest):
    key = 'limit'
    valid = [
        0,
        1,
        1000,
    ]
    invalid = [
        -1,
        0.9,
        'test',
        '',
        []
    ]


class FeaturesKeyTest(_ConfParserTest):
    key = 'features'
    valid = [
        {
            'enabled': {
                'test': {},
                'test2': {
                    'test': 2,
                }
            }
        },
    ]
    invalid = [
        {
            'enabled': [],
        },
        {
            'enabled': {
                'test': [],
            }
        },
        {
            'default_params': {}
        },
        {
            'enabled': {
                'test': {},
            },
            'default_params': {
                1: 1
            }
        }
    ]



"""
Some more complex, combination tests (or: optional keys)
"""

class OutputFileKeyTest(_OptionalConfParserTest):
    key = 'output_file'
    valid = ['string']
    invalid = ['', 0]


class IgnoreStartKeyTest(_ConfParserTest):
    key = 'ignore_start'
    valid = [10, 9001]
    invalid = ['', -1, 0.4]


class IgnoreNumberKeyTest(_ConfParserTest):
    key = 'ignore_number'
    valid = [10, 9001]
    invalid = ['', -1, 0.4]
