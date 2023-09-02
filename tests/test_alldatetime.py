import unittest

from alldatetime.alldatetime import alldate, alldatetime, alltime

connection = ""
class TestAllDateTime(unittest.TestCase):

    def test_all_date(self):
        timestamps = [
            ((1970, 1, 1), 0),
            ((1, 1, 1), -62135596800),
            ((-1, 12, 31), -62135683200),
            ((-1, 2, 29), -62162121600),
            ((-5, 2, 29), -62288352000),
            ((-4001, 2, 29), -188389929600),
        ]
        for date, timestamp in timestamps:
            ad = alldate(*date)
            self.assertEqual(int(timestamp), int(ad.timestamp))

            ad = alldate.fromtimestamp(timestamp)
            self.assertEqual(date, (ad.year, ad.month, ad.day))
            self.assertEqual(int(timestamp), int(ad.timestamp))

    def test_all_datetime(self):
        timestamps = [
            ((1970, 1, 1, 0, 0, 0, 0), 0),
            ((1970, 1, 1, 0, 0, 1, 0), 1),
            ((-1234, 8, 1, 14, 29, 18, 0), -101058571842),
            ((-4001, 1, 29, 15, 51, 30, 0), -188392550910),
            ((-5, 2, 29, 15, 51, 30, 0), -62288294910),
            ((-1, 12, 31, 23, 59, 59, 0), -62135596801),
            ((1, 1, 1, 0, 0, 0, 0), -62135596800),
            ((2023, 12, 29, 15, 51, 30, 0), 1703865090),
        ]
        for datetime, timestamp in timestamps:
            adt = alldatetime(*datetime)
            self.assertEqual(int(adt.timestamp), int(timestamp))

            adt = alldatetime.fromtimestamp(timestamp)
            self.assertEqual(datetime, (adt.year, adt.month, adt.day, adt.hour, adt.minute, adt.second, adt.microsecond))
            self.assertEqual(int(adt.timestamp), int(timestamp))

    def test_alldate_comparisons(self):
        dates = [
            # alldate1, alldate2, equal, less than, less than or equal
            (alldate(1, 1, 1), alldate(1, 1, 1), True, False, True),
            (alldate(1, 1, 2), alldate(1, 1, 1), False, False, False),
            (alldate(1, 2, 1), alldate(1, 1, 1), False, False, False),
            (alldate(2, 1, 1), alldate(1, 1, 1), False, False, False),
            (alldate(1, 1, 1), alldate(1, 1, 2), False, True, True),
            (alldate(1, 1, 1), alldate(1, 2, 1), False, True, True),
            (alldate(1, 1, 1), alldate(2, 1, 1), False, True, True),
        ]
        for alldate1, alldate2, equal, lt, le in dates:
            self.assertEqual(alldate1 == alldate2, equal)
            self.assertEqual(alldate1 < alldate2, lt)
            self.assertEqual(alldate1 <= alldate2, le)
            self.assertEqual(alldate1 > alldate2, not le)
            self.assertEqual(alldate1 >= alldate2, not lt)

            self.assertEqual(alldate2 == alldate1, equal)
            self.assertEqual(alldate2 < alldate1, not le)
            self.assertEqual(alldate2 <= alldate1, not lt)
            self.assertEqual(alldate2 > alldate1, lt)
            self.assertEqual(alldate2 >= alldate1, le)

    def test_alltime_comparisons(self):
        dates = [
            # alltime1, alltime2, equal, less than, less than or equal
            (alltime(14, 10, 10, 1), alltime(14, 10, 10, 1), True, False, True),
            (alltime(14, 10, 10, 2), alltime(14, 10, 10, 1), False, False, False),
            (alltime(14, 10, 11, 1), alltime(14, 10, 10, 1), False, False, False),
            (alltime(14, 11, 10, 1), alltime(14, 10, 10, 1), False, False, False),
            (alltime(15, 10, 10, 1), alltime(14, 10, 10, 1), False, False, False),
            (alltime(14, 10, 10, 1), alltime(14, 10, 10, 2), False, True, True),
            (alltime(14, 10, 10, 1), alltime(14, 10, 11, 1), False, True, True),
            (alltime(14, 10, 10, 1), alltime(14, 11, 10, 1), False, True, True),
            (alltime(14, 10, 10, 1), alltime(15, 10, 10, 1), False, True, True),
        ]
        for alltime1, alltime2, equal, lt, le in dates:
            self.assertEqual(alltime1 == alltime2, equal)
            self.assertEqual(alltime1 < alltime2, lt)
            self.assertEqual(alltime1 <= alltime2, le)
            self.assertEqual(alltime1 > alltime2, not le)
            self.assertEqual(alltime1 >= alltime2, not lt)

            self.assertEqual(alltime2 == alltime1, equal)
            self.assertEqual(alltime2 < alltime1, not le)
            self.assertEqual(alltime2 <= alltime1, not lt)
            self.assertEqual(alltime2 > alltime1, lt)
            self.assertEqual(alltime2 >= alltime1, le)

    def test_alldatetime_comparisons(self):
        dates = [
            # alldatetime1, alldatetime2, equal, less than, less than or equal
            (alldatetime(1, 1, 1, 14, 10, 10, 1), alldatetime(1, 1, 1, 14, 10, 10, 1), True, False, True),
            (alldatetime(1, 1, 1, 14, 10, 10, 2), alldatetime(1, 1, 1, 14, 10, 10, 1), False, False, False),
            (alldatetime(1, 1, 2, 14, 10, 10, 1), alldatetime(1, 1, 1, 14, 10, 10, 1), False, False, False),
            (alldatetime(1, 1, 1, 14, 10, 10, 1), alldatetime(1, 1, 1, 14, 10, 10, 2), False, True, True),
            (alldatetime(1, 1, 1, 14, 10, 10, 1), alldatetime(1, 1, 2, 14, 10, 10, 1), False, True, True),
        ]
        for alldatetime1, alldatetime2, equal, lt, le in dates:
            self.assertEqual(alldatetime1 == alldatetime2, equal)
            self.assertEqual(alldatetime1 < alldatetime2, lt)
            self.assertEqual(alldatetime1 <= alldatetime2, le)
            self.assertEqual(alldatetime1 > alldatetime2, not le)
            self.assertEqual(alldatetime1 >= alldatetime2, not lt)

            self.assertEqual(alldatetime2 == alldatetime1, equal)
            self.assertEqual(alldatetime2 < alldatetime1, not le)
            self.assertEqual(alldatetime2 <= alldatetime1, not lt)
            self.assertEqual(alldatetime2 > alldatetime1, lt)
            self.assertEqual(alldatetime2 >= alldatetime1, le)
