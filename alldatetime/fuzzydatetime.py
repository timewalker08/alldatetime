from datetime import timedelta
from enum import Enum
from operator import index as _index

from alldatetime.alldatetime import (
    _check_month,
    _check_year,
    _days_in_month,
    alldate,
    alldateperiod,
)


class PrecisionUnit(Enum):
    Year = "Year"
    Month = "Month"
    Day = "Day"
    # Hour = "Hour"
    # Minute = "Minute"
    # Second = "Second"


class Precision:
    def __init__(self, num: int, unit: PrecisionUnit):
        if num < 0:
            raise ValueError("num should not be negative.")
        self._num = num
        self._unit = unit

    @property
    def num(self):
        return self._num

    @property
    def unit(self):
        return self._unit


class fuzzydate:
    def __init__(
        self,
        year: int = None,
        month: int = None,
        day: int = None,
        precision: Precision = None,
        forward_precision: Precision = None,
        backward_precision: Precision = None,
    ):
        (
            self._year,
            self._month,
            self._day,
            self._precision,
            self._forward_precision,
            self._backward_precision,
        ) = self._check_parameters(
            year, month, day, precision, forward_precision, backward_precision
        )
        self._anchor = alldate(self._year, self._month or 1, self._day or 1)

    def _check_parameters(
        self,
        year: int = None,
        month: int = None,
        day: int = None,
        precision: Precision = None,
        forward_precision: Precision = None,
        backward_precision: Precision = None,
    ):
        if year is None:
            raise ValueError("year should not be None.")
        _check_year(year)
        inferred_forward_precision = Precision(0, PrecisionUnit.Year)
        inferred_backward_precision = Precision(1, PrecisionUnit.Year)
        if month is not None:
            _check_month(month)
            inferred_forward_precision = Precision(0, PrecisionUnit.Month)
            inferred_backward_precision = Precision(1, PrecisionUnit.Month)
        if day is not None:
            if month is None:
                raise ValueError("month should not be None if day is not None.")
            day = _index(day)
            dim = _days_in_month(year, month)
            if not 1 <= day <= dim:
                raise ValueError(f"day must be in 1..{dim}")
            inferred_forward_precision = Precision(0, PrecisionUnit.Day)
            inferred_backward_precision = Precision(1, PrecisionUnit.Day)
        if forward_precision is None:
            forward_precision = precision or inferred_forward_precision
        if backward_precision is None:
            backward_precision = precision or inferred_backward_precision

        return (
            year,
            month,
            day,
            precision,
            forward_precision,
            backward_precision,
        )

    @property
    def year(self):
        return self._year

    @property
    def month(self):
        return self._month

    @property
    def day(self):
        return self._day

    @property
    def anchor(self):
        return self._anchor

    @property
    def forward_precision(self):
        return self._forward_precision

    @property
    def backward_precision(self):
        return self._backward_precision

    def to_alldateperiod(self) -> alldateperiod:
        forward_timedelta = self._precision_to_timedelta(self.forward_precision)
        backward_timedelta = self._precision_to_timedelta(self.backward_precision)
        return alldateperiod(
            self.anchor - forward_timedelta, self.anchor + backward_timedelta
        )

    def _precision_to_timedelta(self, precision: Precision):
        if precision.unit == PrecisionUnit.Year:
            return timedelta(days=precision.num * 365)
        if precision.unit == PrecisionUnit.Month:
            return timedelta(days=int(precision.num * 30.5))
        if precision.unit == PrecisionUnit.Day:
            return timedelta(days=precision.num)

    def to_alldateperiod_timestamps(self) -> tuple[float, float]:
        period = self.to_alldateperiod()
        return (period.start_date.timestamp, period.end_date.timestamp)

    def overlap_with(self, other) -> bool:
        if not isinstance(other, fuzzydate):
            return False
        self_period = self.to_alldateperiod()
        other_period = other.to_alldateperiod()
        return self_period.overlap_with(other_period)


class fuzzydateperiod:
    __slots__ = "_start_date", "_end_date", "_hashcode"

    def __init__(self, start_date: fuzzydate, end_date: fuzzydate):
        if start_date is None:
            raise ValueError("start_date should not be None.")
        if end_date is None:
            raise ValueError("end_date should not be None.")
        if start_date.anchor > end_date.anchor:
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

    def cover(self, date: fuzzydate):
        if date is None:
            raise ValueError("date should not be None.")
        start_period = self._start_date.to_alldateperiod()
        end_period = self._end_date.to_alldateperiod()
        date_period = date.to_alldateperiod()
        start_date = start_period.start_date
        end_date = end_period.end_date
        return not (
            start_date >= date_period.end_date or end_date <= date_period.start_date
        )
