import math as _math
import time as _time
from datetime import date, datetime, time, timedelta
from operator import index as _index

__all__ = ("alldate", "alltime", "alldatetime")


def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


BCENDING = " BC"
ADENDING = " AD"

_MONTHNAMES = [
    None,
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
_DAYNAMES = [None, "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
# -1 is a placeholder for indexing purposes.
_DAYS_IN_MONTH = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
_DAYS_BEFORE_MONTH = [-1]  # -1 is a placeholder for indexing purposes.

SECONDSPERHOUR = 3600
SECONDSPERMINUTE = 60

dbm = 0
for dim in _DAYS_IN_MONTH[1:]:
    _DAYS_BEFORE_MONTH.append(dbm)
    dbm += dim
del dbm, dim


def _check_year(year: int) -> int:
    year = _index(year)
    if year == 0:
        raise ValueError("year should not be 0", year)
    return year


def _check_month(month: int) -> int:
    month = _index(month)
    if not 1 <= month <= 12:
        raise ValueError("month must be in 1..12", month)
    return month


def _is_leap(year: int):
    "year -> 1 if leap year, else 0."
    if year < 0:
        year += 1
        year = -year
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _days_before_year(year):
    "year -> number of days before January 1st of year."
    if year > 0:
        y = year - 1
        return y * 365 + y // 4 - y // 100 + y // 400
    if year < 0:
        y = -year
        return -(y * 365 + 1 + (y - 1) // 4 - (y - 1) // 100 + (y - 1) // 400)


def _days_in_month(year, month):
    "year, month -> number of days in that month in that year."
    month = _check_month(month)
    if month == 2 and _is_leap(year):
        return 29
    return _DAYS_IN_MONTH[month]


def _days_before_month(year, month):
    "year, month -> number of days in year preceding first day of month."
    month = _check_month(month)
    return _DAYS_BEFORE_MONTH[month] + (month > 2 and _is_leap(year))


_DI400Y = _days_before_year(401)  # number of days in 400 years
_DI100Y = _days_before_year(101)  #    "    "   "   " 100   "
_DI4Y = _days_before_year(5)  #    "    "   "   "   4   "


def _ymd2ord(year: int, month: int, day: int) -> int:
    "year, month, day -> ordinal, considering 01-Jan-0001 as day 0."
    year, month, day = _check_date_fields(year, month, day)
    return _days_before_year(year) + _days_before_month(year, month) + day - 1


def _ord2ymd(n):
    "ordinal -> (year, month, day), considering 01-Jan-0001 as day 0."

    # n is a 0-based index, starting at 1-Jan-1.  The pattern of leap years
    # repeats exactly every 400 years.  The basic strategy is to find the
    # closest 400-year boundary at or before n, then work with the offset
    # from that boundary to n.  Life is much clearer if we subtract 1 from
    # n first -- then the values of n at 400-year boundaries are exactly
    # those divisible by _DI400Y:
    #
    #     D  M   Y            n              n-1
    #     -- --- ----        ----------     ----------------
    #     31 Dec -400        -_DI400Y       -_DI400Y -1
    #      1 Jan -399         -_DI400Y +1   -_DI400Y      400-year boundary
    #     ...
    #     30 Dec  000        -1             -2
    #     31 Dec  000         0             -1
    #      1 Jan  001         1              0            400-year boundary
    #      2 Jan  001         2              1
    #      3 Jan  001         3              2
    #     ...
    #     31 Dec  400         _DI400Y        _DI400Y -1
    #      1 Jan  401         _DI400Y +1     _DI400Y      400-year boundary
    # n -= 1
    n400, n = divmod(n, _DI400Y)
    if n400 >= 0:
        year = n400 * 400 + 1  # ..., -399, 1, 401, ...
    else:
        year = n400 * 400

    # Now n is the (non-negative) offset, in days, from January 1 of year, to
    # the desired date.  Now compute how many 100-year cycles precede n.
    # Note that it's possible for n100 to equal 4!  In that case 4 full
    # 100-year cycles precede the desired day, which implies the desired
    # day is December 31 at the end of a 400-year cycle.
    n100, n = divmod(n, _DI100Y)

    # Now compute how many 4-year cycles precede it.
    n4, n = divmod(n, _DI4Y)

    # And now how many single years.  Again n1 can be 4, and again meaning
    # that the desired day is December 31 at the end of the 4-year cycle.
    n1, n = divmod(n, 365)

    year += n100 * 100 + n4 * 4 + n1
    if n1 == 4 or n100 == 4:
        assert n == 0
        return year - 1, 12, 31

    # Now the year is correct, and n is the offset from January 1.  We find
    # the month via an estimate that's either exact or one too large.
    leapyear = n1 == 3 and (n4 != 24 or n100 == 3)
    assert leapyear == _is_leap(year)
    month = (n + 50) >> 5
    preceding = _DAYS_BEFORE_MONTH[month] + (month > 2 and leapyear)
    if preceding > n:  # estimate is too large
        month -= 1
        preceding -= _DAYS_IN_MONTH[month] + (month == 2 and leapyear)
    n -= preceding
    assert 0 <= n < _days_in_month(year, month)

    # Now the year and month are correct, and n is the offset from the
    # start of that month:  we're done!
    return year, month, n + 1


def _build_struct_time(y, m, d, hh, mm, ss, dstflag):
    wday = (_ymd2ord(y, m, d) + 7) % 7
    dnum = _days_before_month(y, m) + d
    return _time.struct_time((y, m, d, hh, mm, ss, wday, dnum, dstflag))


def _days_in_month(year, month):
    "year, month -> number of days in that month in that year."
    month = _check_month(month)
    if month == 2 and _is_leap(year):
        return 29
    return _DAYS_IN_MONTH[month]


def _check_date_fields(year: int, month: int, day: int) -> tuple[int, int, int]:
    year = _check_year(year)
    month = _check_month(month)
    day = _index(day)
    dim = _days_in_month(year, month)
    if not 1 <= day <= dim:
        raise ValueError("day must be in 1..%d" % dim, day)
    return year, month, day


def _check_time_fields(hour, minute, second, microsecond):
    hour = _index(hour)
    minute = _index(minute)
    second = _index(second)
    microsecond = _index(microsecond)
    if not 0 <= hour <= 23:
        raise ValueError("hour must be in 0..23", hour)
    if not 0 <= minute <= 59:
        raise ValueError("minute must be in 0..59", minute)
    if not 0 <= second <= 59:
        raise ValueError("second must be in 0..59", second)
    if not 0 <= microsecond <= 999999:
        raise ValueError("microsecond must be in 0..999999", microsecond)
    return hour, minute, second, microsecond


class alldate:
    __slots__ = "_year", "_month", "_day", "_hashcode", "_timestamp"

    def __init__(self, year: int, month: int, day: int):
        year, month, day = _check_date_fields(year, month, day)
        self._year = year
        self._month = month
        self._day = day
        if year < 0:
            year += 1
        self._timestamp = _time.mktime((year, month, day, 0, 0, 0, 0, 0, 0))
        self._hashcode = -1

    @classmethod
    def fromtimestamp(cls, timestamp: int):
        "Construct a date from a POSIX timestamp (like time.time())."
        y, m, d, hh, mm, ss, weekday, jday, dst = _time.gmtime(timestamp)
        if y <= 0:
            y -= 1
        return cls(y, m, d)

    @classmethod
    def today(cls):
        "Construct a date from time.time()."
        t = _time.time()
        return cls.fromtimestamp(t)

    @classmethod
    def fromordinal(cls, n: int):
        """Construct a date from a proleptic Gregorian ordinal.

        January 1 of year 1 is day 0.  Only the year, month and day are
        non-zero in the result.
        """
        y, m, d = _ord2ymd(n)
        return cls(y, m, d)

    @property
    def year(self) -> int:
        """year (1-9999)"""
        return self._year

    @property
    def month(self) -> int:
        """month (1-12)"""
        return self._month

    @property
    def day(self) -> int:
        """day (1-31)"""
        return self._day

    @property
    def timestamp(self) -> float:
        return self._timestamp

    # Comparisons of date objects with other.

    def __eq__(self, other):
        if isinstance(other, alldate):
            return self._cmp(other) == 0
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, alldate):
            return self._cmp(other) <= 0
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, alldate):
            return self._cmp(other) < 0
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, alldate):
            return self._cmp(other) >= 0
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, alldate):
            return self._cmp(other) > 0
        return NotImplemented

    def _cmp(self, other):
        assert isinstance(other, alldate)
        y, m, d = self._year, self._month, self._day
        y2, m2, d2 = other._year, other._month, other._day
        return _cmp((y, m, d), (y2, m2, d2))

    def __hash__(self):
        "Hash."
        if self._hashcode == -1:
            self._hashcode = hash(self._getstate())
        return self._hashcode

    def _getstate(self):
        yhi, ylo = divmod(self._year, 256)
        return (bytes([yhi, ylo, self._month, self._day]),)

    def toordinal(self):
        """Return proleptic Gregorian ordinal for the year, month and day.

        January 1 of year 1 is day 0.  Only the year, month and day values
        contribute to the result.
        """
        return _ymd2ord(self._year, self._month, self._day)

    def __add__(self, other):
        "Add a date to a timedelta."
        if isinstance(other, timedelta):
            o = self.toordinal() + other.days
            return type(self).fromordinal(o)
        return NotImplemented

    __radd__ = __add__

    def __sub__(self, other):
        """Subtract two dates, or a date and a timedelta."""
        if isinstance(other, timedelta):
            return self + timedelta(-other.days)
        if isinstance(other, alldate):
            days1 = self.toordinal()
            days2 = other.toordinal()
            return timedelta(days1 - days2)
        return NotImplemented

    def isoformat(self):
        """Return the date formatted according to ISO.

        This is 'YYYY-MM-DD'.

        References:
        - http://www.w3.org/TR/NOTE-datetime
        - http://www.cl.cam.ac.uk/~mgk25/iso-time.html
        """
        formater = "%04d-%02d-%02d" if self._year > 0 else "%05d-%02d-%02d"
        return formater % (self._year, self._month, self._day)

    __str__ = isoformat

    def strftime(self, format):
        date_string = date(abs(self.year), self.month, self.day).strftime(format)
        if self.year < 0:
            date_string += BCENDING
        else:
            date_string += ADENDING

        return date_string


class alldateperiod:
    """
    Represents a time interval, consisting of a start time and an end time, forming an open-closed interval.
    """

    __slots__ = "_start_date", "_end_date", "_hashcode"

    def __init__(self, start_date: alldate, end_date: alldate):
        if start_date is None:
            raise ValueError("start_date should not be None.")
        if end_date is None:
            raise ValueError("end_date should not be None.")
        if start_date > end_date:
            raise ValueError("start_date should be earlier than end_date.")
        self._start_date = start_date
        self._end_date = end_date
        self._hashcode = -1

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    def overlap_with(self, other) -> bool:
        if not isinstance(other, alldateperiod):
            return False
        return not (
            self.end_date <= other.start_date or self.start_date >= other.end_date
        )
    
    def cover(self, date: alldate) -> bool:
        if not isinstance(date, alldate):
            raise ValueError("date should be of type alldate.")
        return date >= self._start_date and date < self._end_date

    def __eq__(self, other):
        if isinstance(other, alldateperiod):
            return (
                self.start_date == other.start_date and self.end_date == other.end_date
            )
        else:
            return NotImplemented

    def __hash__(self):
        if self._hashcode == -1:
            t = self
            self._hashcode = hash(t._getstate()[0])
        return self._hashcode

    def _getstate(self):
        yhi1, ylo1 = divmod(self.start_date.year, 256)
        yhi2, ylo2 = divmod(self.end_date.year, 256)
        return (
            bytes(
                [
                    yhi1,
                    ylo1,
                    self.start_date.month,
                    self.start_date.day,
                    yhi2,
                    ylo2,
                    self.end_date.month,
                    self.end_date.day,
                ]
            ),
        )


def _format_time(hh, mm, ss, us, timespec="auto"):
    specs = {
        "hours": "{:02d}",
        "minutes": "{:02d}:{:02d}",
        "seconds": "{:02d}:{:02d}:{:02d}",
        "milliseconds": "{:02d}:{:02d}:{:02d}.{:03d}",
        "microseconds": "{:02d}:{:02d}:{:02d}.{:06d}",
    }

    if timespec == "auto":
        # Skip trailing microseconds when us==0.
        timespec = "microseconds" if us else "seconds"
    elif timespec == "milliseconds":
        us //= 1000
    try:
        fmt = specs[timespec]
    except KeyError:
        raise ValueError("Unknown timespec value")
    else:
        return fmt.format(hh, mm, ss, us)


class alltime:
    __slots__ = "_hour", "_minute", "_second", "_microsecond", "_hashcode"

    def __init__(self, hour, minute, second, microsecond=0):
        self._hour, self._minute, self._second, self._microsecond = _check_time_fields(
            hour, minute, second, microsecond
        )
        self._hashcode = -1

    @property
    def hour(self):
        """hour (0-23)"""
        return self._hour

    @property
    def minute(self):
        """minute (0-59)"""
        return self._minute

    @property
    def second(self):
        """second (0-59)"""
        return self._second

    @property
    def microsecond(self):
        """microsecond (0-999999)"""
        return self._microsecond

    def seconds_from_zero_hour(self):
        return (
            self._hour * SECONDSPERHOUR
            + self._minute * SECONDSPERMINUTE
            + self._second
            + self._microsecond / 1e6
        )

    def __eq__(self, other):
        if isinstance(other, alltime):
            return self._cmp(other) == 0
        else:
            return NotImplemented

    def __le__(self, other):
        if isinstance(other, alltime):
            return self._cmp(other) <= 0
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, alltime):
            return self._cmp(other) < 0
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, alltime):
            return self._cmp(other) >= 0
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, alltime):
            return self._cmp(other) > 0
        else:
            return NotImplemented

    def _cmp(self, other):
        assert isinstance(other, alltime)

        return _cmp(
            (self._hour, self._minute, self._second, self._microsecond),
            (other._hour, other._minute, other._second, other._microsecond),
        )

    def __hash__(self):
        """Hash."""
        if self._hashcode == -1:
            t = self
            self._hashcode = hash(t._getstate()[0])
        return self._hashcode

    def _getstate(self, protocol=3):
        us2, us3 = divmod(self._microsecond, 256)
        us1, us2 = divmod(us2, 256)
        h = self._hour
        basestate = bytes([h, self._minute, self._second, us1, us2, us3])
        return (basestate,)

    def isoformat(self, timespec="auto"):
        """Return the time formatted according to ISO.

        The full format is 'HH:MM:SS.mmmmmm+zz:zz'. By default, the fractional
        part is omitted if self.microsecond == 0.

        The optional argument timespec specifies the number of additional
        terms of the time to include. Valid options are 'auto', 'hours',
        'minutes', 'seconds', 'milliseconds' and 'microseconds'.
        """
        s = _format_time(
            self._hour, self._minute, self._second, self._microsecond, timespec
        )

        return s

    __str__ = isoformat

    def strftime(self, format):
        return time(self.hour, self.minute, self.second, self.microsecond).strftime(
            format
        )


class alldatetime:
    __slots__ = ("_date", "_time", "_hashcode")

    def __init__(
        self,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
    ):
        self._date = alldate(year, month, day)
        self._time = alltime(hour, minute, second, microsecond)
        self._hashcode = -1

    @classmethod
    def fromtimestamp(cls, timestamp: int):
        frac, timestamp = _math.modf(timestamp)
        us = round(frac * 1e6)
        if us >= 1000000:
            timestamp += 1
            us -= 1000000
        elif us < 0:
            timestamp -= 1
            us += 1000000
        y, m, d, hh, mm, ss, weekday, jday, dst = _time.gmtime(timestamp)
        if y <= 0:
            y -= 1
        return cls(y, m, d, hh, mm, ss, us)

    @property
    def year(self):
        """year (1-9999)"""
        return self._date.year

    @property
    def month(self):
        """month (1-12)"""
        return self._date.month

    @property
    def day(self):
        """day (1-31)"""
        return self._date.day

    @property
    def hour(self):
        """hour (0-23)"""
        return self._time.hour

    @property
    def minute(self):
        """minute (0-59)"""
        return self._time.minute

    @property
    def second(self):
        """second (0-59)"""
        return self._time.second

    @property
    def microsecond(self):
        """microsecond (0-999999)"""
        return self._time.microsecond

    @property
    def timestamp(self):
        return self._date.timestamp + self._time.seconds_from_zero_hour()

    def date(self) -> alldate:
        "Return the date part."
        return alldate(self._date.year, self._date.month, self._date.day)

    def time(self) -> alltime:
        return alltime(
            self._time.hour,
            self._time.minute,
            self._time.second,
            self._time.microsecond,
        )

    def __eq__(self, other):
        if isinstance(other, alldatetime):
            return self._cmp(other) == 0
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, alldatetime):
            return self._cmp(other) <= 0
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, alldatetime):
            return self._cmp(other) < 0
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, alldatetime):
            return self._cmp(other) >= 0
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, alldatetime):
            return self._cmp(other) > 0
        return NotImplemented

    def _cmp(self, other):
        assert isinstance(other, alldatetime)
        date_cmp = self._date._cmp(other._date)
        if date_cmp == 0:
            return self._time._cmp(other._time)
        return date_cmp

    def __hash__(self):
        if self._hashcode == -1:
            t = self
            self._hashcode = hash(t._getstate()[0])
        return self._hashcode

    def _getstate(self, protocol=3):
        yhi, ylo = divmod(self._year, 256)
        us2, us3 = divmod(self._microsecond, 256)
        us1, us2 = divmod(us2, 256)
        m = self._month
        basestate = bytes(
            [
                yhi,
                ylo,
                m,
                self._day,
                self._hour,
                self._minute,
                self._second,
                us1,
                us2,
                us3,
            ]
        )
        return (basestate,)

    def isoformat(self, timespec="auto"):
        """Return the time formatted according to ISO.

        The full format is 'HH:MM:SS.mmmmmm+zz:zz'. By default, the fractional
        part is omitted if self.microsecond == 0.

        The optional argument timespec specifies the number of additional
        terms of the time to include. Valid options are 'auto', 'hours',
        'minutes', 'seconds', 'milliseconds' and 'microseconds'.
        """
        s = self._date.isoformat() + " " + self._time.isoformat(timespec)

        return s

    __str__ = isoformat

    @classmethod
    def strptime(cls, date_string: str, format: str):
        bc = False
        if date_string.endswith(BCENDING):
            bc = True
            date_string = date_string.rstrip(BCENDING)
        if date_string.endswith(ADENDING):
            bc = False
            date_string = date_string.rstrip(ADENDING)
        date_string = date_string.strip()
        parsed_date = datetime.strptime(date_string, format)
        year = parsed_date.year if not bc else -parsed_date.year
        return cls(
            year,
            parsed_date.month,
            parsed_date.day,
            parsed_date.hour,
            parsed_date.minute,
            parsed_date.second,
            parsed_date.microsecond,
        )

    def strftime(self, format):
        date_string = datetime(
            abs(self.year),
            self.month,
            self.day,
            self.hour,
            self.minute,
            self.second,
            self.microsecond,
        ).strftime(format)
        if self.year < 0:
            date_string += BCENDING
        else:
            date_string += ADENDING

        return date_string
