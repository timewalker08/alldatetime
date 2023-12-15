import unittest

from alldatetime.alldatetime import alldate, alldateperiod
from alldatetime.fuzzydatetime import fuzzydate, Precision, PrecisionUnit, fuzzydateperiod
from datetime import timedelta


class TestFuzzyDate(unittest.TestCase):
    def test_dateperiod(self):
        fuzzydates = [
            (fuzzydate(2023), alldateperiod(alldate(2023, 1, 1), alldate(2024, 1, 1))),
            (
                fuzzydate(2023, 1),
                alldateperiod(alldate(2023, 1, 1), alldate(2023, 1, 31)),
            ),
            (
                fuzzydate(2023, 1, 1),
                alldateperiod(alldate(2023, 1, 1), alldate(2023, 1, 2)),
            ),
            (
                fuzzydate(
                    2023, 1, 1, precision=Precision(num=2, unit=PrecisionUnit.Day)
                ),
                alldateperiod(alldate(2022, 12, 30), alldate(2023, 1, 3)),
            ),
        ]
        for fuzzy_date, date_period in fuzzydates:
            self.assertEqual(fuzzy_date.to_alldateperiod(), date_period)

    def test_overlap(self):
        fuzzydates = [
            (fuzzydate(202), fuzzydate(203), False),
            (fuzzydate(202), fuzzydate(202), True),
            (fuzzydate(202, 1), fuzzydate(203), False),
            (fuzzydate(202, 1), fuzzydate(202), True),
            (fuzzydate(202, 1, 1), fuzzydate(202), True),
            (fuzzydate(202, 12, 31), fuzzydate(202), True),
        ]
        for fuzzy_date1, fuzzy_date2, overlap in fuzzydates:
            self.assertEqual(fuzzy_date1.overlap_with(fuzzy_date2), overlap)
            self.assertEqual(fuzzy_date2.overlap_with(fuzzy_date1), overlap)

    def test_fuzzdateperiod(self):
        with self.assertRaises(ValueError):
            fuzzydateperiod(None, None)
        with self.assertRaises(ValueError):
            fuzzydateperiod(None, fuzzydate(202))
        with self.assertRaises(ValueError):
            fuzzydateperiod(fuzzydate(202), None)
        with self.assertRaises(ValueError):
            fuzzydateperiod(fuzzydate(202, 2), fuzzydate(202))
        period = fuzzydateperiod(fuzzydate(202, 1), fuzzydate(202, 5))
        self.assertTrue(period.cover(fuzzydate(202, 3)))
        self.assertTrue(period.cover(fuzzydate(202, 1)))
        self.assertFalse(period.cover(fuzzydate(202, 6)))
