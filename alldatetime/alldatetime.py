import math as _math
import time as _time
from datetime import date, datetime, time
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
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _days_offset_from_year_1(year: int):
    "year -> number of days between January 1st of year {year} and January 1st of year 1."
    year = _check_year(year)
    if year > 0:
        y = year - 1
        return y * 365 + y // 4 - y // 100 + y // 400
    else:
        y = -year
        return -(y * 365 + y // 4 - y // 100 + y // 400)


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


def _ymd2ord(year: int, month: int, day: int) -> int:
    "year, month, day -> ordinal, considering 01-Jan-0001 as day 1."
    year, month, day = _check_date_fields(year, month, day)
    return _days_offset_from_year_1(year) + _days_before_month(year, month) + day


def _build_struct_time(y, m, d, hh, mm, ss, dstflag):
    ord = _ymd2ord(y, m, d)
    wday = (_ymd2ord(y, m, d) + 6) % 7
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

    @property
    def year(self):
        """year (1-9999)"""
        return self._year

    @property
    def month(self):
        """month (1-12)"""
        return self._month

    @property
    def day(self):
        """day (1-31)"""
        return self._day

    @property
    def timestamp(self):
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
        return self._hour * SECONDSPERHOUR + self._minute * SECONDSPERMINUTE + self._second + self._microsecond / 1e6

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
        return time(self.hour, self.minute, self.second, self.microsecond).strftime(format)


class alldatetime():
    __slots__ = ("_date", "_time")

    def __init__(self, year, month=None, day=None, hour=0, minute=0, second=0, microsecond=0):
        self._date = alldate(year, month, day)
        self._time = alltime(hour, minute, second, microsecond)

    @classmethod
    def fromtimestamp(cls, timestamp):
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
    
    def date(self):
        "Return the date part."
        return alldate(self._date.year, self._date.month, self._date.day)
    
    def time(self):
        return alltime(self._time.hour, self._time.minute, self._time.second, self._time.microsecond)
    
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
    def strptime(cls, date_string, format):
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
        return cls(year, parsed_date.month, parsed_date.day, parsed_date.hour, parsed_date.minute, parsed_date.second, parsed_date.microsecond)

    def strftime(self, format):
        date_string = datetime(abs(self.year), self.month, self.day, self.hour, self.minute, self.second, self.microsecond).strftime(format)
        if self.year < 0:
            date_string += BCENDING
        else:
            date_string += ADENDING

        return date_string
