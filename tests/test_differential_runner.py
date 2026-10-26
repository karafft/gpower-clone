import unittest
from test_differential import compare


class ComparisonTests(unittest.TestCase):
    def test_integer_type_is_exact(self):
        self.assertTrue(compare({"n1": 88.0}, {"n1": 88}))
        self.assertTrue(compare({"n1": True}, {"n1": 1}))
        self.assertEqual(compare({"n1": 88}, {"n1": 88}), [])

    def test_tolerances_and_missing(self):
        self.assertEqual(compare({"power": .95+1e-8}, {"power": .95}), [])
        self.assertTrue(compare({"power": .96}, {"power": .95}))
        self.assertTrue(compare({}, {"power": .95}))
        self.assertTrue(compare({"power": float("nan")}, {"power": .95}))
