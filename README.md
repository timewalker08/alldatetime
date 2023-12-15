# alldatetime
## Introduction
This is a lightweight Python library for representing time and dates, with no restrictions on the year range. (Unlike the datetime library in CPython, which has a year range from 1 to 9999.) It also supports fuzzy dates, allowing for representation of uncertain times (i.e., you can specify only the year, month, or day). For example, it can represent dates like 1912, or March 1912, etc. Some parts of the code are referenced from CPython's datetime implementation.  
Please NOTE that this library currently does not support time zones currently.

## Installation
To install this library, run the following command:  

    pip install alldatetime  

## Types Overview
- `alldatetime.alldatetime.alldate`: A class used to represent dates.
- `alldatetime.alldatetime.alltime`: A class used to represent time.
- `alldatetime.alldatetime.alldatetime`: A class used to represent date and time.
- `alldatetime.alldatetime.alldateperiod`: Used to represent a time interval by specifying a start time and an end time.
- `alldatetime.fuzzydatetime.fuzzydate`: Used to represent a fuzzy date, such as the year 1950, or June 1950, etc.
- `alldatetime.fuzzydatetime.fuzzydateperiod`: Used to represent a fuzzy date range, such as from 1950 to 1980, or from June 1950 to September 1950, etc.

## alldate
`alldate` is used to represent dates by specifying year, month and day.

### Methods and Constructor

#### `__init__(self, year: int, month: int, day: int)`
Constructor of class `alldate`.  
- `year`: The year of the date. No limitation. Use negative numbers to represent years before the Common Era (BC).
- `month`: The month of the date. Ranging from 1 to 12. A ValueError will be raised if month is out of range.
- `day`: The day of the date. The range starts from 1 and goes up to the number of days in the specified month. A ValueError will be raised if month is out of range.

#### classmethod `fromtimestamp(cls, timestamp: int)`
Return an instance of `alldate` corresponding to the POSIX timestamp.
- `timestamp`: POSIX timestamp.
- **Returns**: An instance of `alldate` corresponding to the POSIX timestamp.

Example usage:
```python
from alldatetime.alldatetime import alldate
ad = alldate.fromtimestamp(-111553804800)
print(ad) # -1566-01-01
```

#### `fromordinal(cls, n: int)`
Return an instance of `alldate` from a modified version of proleptic Gregorian ordinal. Ordinal number 0 represents January 1, 1 AD not 1.
- `n`: Ordinal number. Ordinal number 0 represents January 1, 1 AD.
- **Returns**: An instance of `alldate` corresponding to the ordinal number.

Example usage:
```python
from alldatetime.alldatetime import alldate
date = alldate.fromordinal(0)
print(date) # 0001-01-01
date = alldate.fromordinal(-1)
print(date) # -0001-12-31
```

#### `toordinal(self)`
- **Returns**: A modified version of proleptic Gregorian ordinal. Ordinal number 0 represents January 1, 1 AD not 1.

Example usage:
```python
from alldatetime.alldatetime import alldate
date = alldate(1, 1, 1)
ordinal = date.toordinal()
print(ordinal) # 0
date = alldate(-1, 12, 31)
ordinal = date.toordinal()
print(ordinal) # -1
```

### Properties

- `year`: The year of the date.
- `month`: The month of the date.
- `day`: The day of the date.
- `timestamp` The POSIX timestamp of the beginning of the date.


## alltime
`alltime` is used to represent a time by specifying hour, minute, second and millisecond.

### Methods and Constructor

#### `__init__(self, hour, minute, second, microsecond=0)`
Constructor of class `alltime`.  
- `hour`: The hour of the time raning from 0 to 23. A ValueError will be raised if month is out of range.
- `minute`: The minute of the time ranging from 0 to 59. A ValueError will be raised if month is out of range.
- `second`: The second of the time ranging from 0 to 59. A ValueError will be raised if month is out of range.
- `microsecond`: The microsecond of the time raning from 0 to 999999. A ValueError will be raised if month is out of range.

### Properties

- `hour`: The hour of the time.
- `minute`: The minute of the time.
- `second`: The second of the time.
- `microsecond`: The microsecond of the time.

## alldatetime
`alldatetime` is used to represent a date time.

### Methods and Constructor

#### `__init__(self, year: int, month: int, day: int, hour: int=0, minute: int=0, second: int=0, microsecond: int=0)`
Constructor of class `alldatetime`.  
- `year`: The year of the date. No limitation. Use negative numbers to represent years before the Common Era (BC).
- `month`: The month of the date. Ranging from 1 to 12. A ValueError will be raised if month is out of range.
- `day`: The day of the date. The range starts from 1 and goes up to the number of days in the specified month. A ValueError will be raised if month is out of range.
- `hour`: The hour of the time raning from 0 to 23. A ValueError will be raised if month is out of range.
- `minute`: The minute of the time ranging from 0 to 59. A ValueError will be raised if month is out of range.
- `second`: The second of the time ranging from 0 to 59. A ValueError will be raised if month is out of range.
- `microsecond`: The microsecond of the time raning from 0 to 999999. A ValueError will be raised if month is out of range.

#### classmethod `fromtimestamp(cls, timestamp: int)`
Return an instance of `alldatetime` corresponding to the POSIX timestamp.
- `timestamp`: POSIX timestamp.
- **Returns**: An instance of `alldatetime` corresponding to the POSIX timestamp.

Example usage:
```python
from alldatetime.alldatetime import alldatetime
dt = alldatetime.fromtimestamp(-111553854830)
print(dt) # -1567-12-31 10:06:10
dt = alldatetime.fromtimestamp(0)
print(dt) # 1970-01-01 00:00:00
```

#### `date(self) -> alldate`
Return an `alldate` instance representing the date part of the date time.
- **Returns**: An `alldate` instance representing the date part of the date time.

#### `time(self) -> alltime`
Return an `alltime` instance representing the time part of the date time.
- **Returns**: An `alltime` instance representing the time part of the date time.

#### classmethod `strptime(cls, date_string: str, format: str)`
Class method `strptime` creates an alldatetime object from a string representing a date and time and a corresponding format string.
- `date_string`: A string representing a date and time.
- `format`: Corresponding format string.
- **Returns**: An instance of `alldatetime` parsed from the date and time string based on the format string.

Example usage:
```python
from alldatetime.alldatetime import alldatetime
alldatetime.strptime("5000-01-08 08:30:15 BC", "%Y-%m-%d %H:%M:%S")    # alldatetime(-5000, 1, 8, 8, 30, 15)
alldatetime.strptime("5000/01/08 08:30:15 BC", "%Y/%m/%d %H:%M:%S")    # alldatetime(-5000, 1, 8, 8, 30, 15)
alldatetime.strptime("2000-01-08 08:30:15 AD", "%Y-%m-%d %H:%M:%S")    # alldatetime(2000, 1, 8, 8, 30, 15)
alldatetime.strptime("2000-01-08 08:30:15", "%Y-%m-%d %H:%M:%S")       # alldatetime(2000, 1, 8, 8, 30, 15)
```

### Properties

- `year`: The year of the date.
- `month`: The month of the date.
- `day`: The day of the date.
- `hour`: The hour of the time.
- `minute`: The minute of the time.
- `second`: The second of the time.
- `microsecond`: The microsecond of the time.
- `timestamp` The POSIX timestamp of the date time.



## alldateperiod
`alldateperiod` is used to represent a date period, consisting of a start date and an end date, forming an open-closed interval.

### Methods and Constructor

#### `__init__(self, start_date: alldate, end_date: alldate)`
Constructor of class `alldateperiod`.  
- `start_date`: The start date of the date period.
- `end_date`: The end date of the date period.

#### `overlap_with(self, other)`
Check whether the date period overlaps with another date period.
- `other`: An instance of `alldateperiod`.
- **Returns**: Whether the date period overlaps with the date period passed.

Example usage:
```python
from alldatetime.alldatetime import alldate, alldateperiod
period = alldateperiod(alldate(2023, 12, 1), alldate(2023, 12, 5))
other_period = alldateperiod(alldate(2023, 10, 10), alldate(2023, 12, 3))
overlap = period.overlap_with(other_period)  # True
```

#### `cover(self, date: alldate) -> bool`
Check whether the date period covers a date.
- `date`: An instance of `alldate`.
- **Returns**: Whether the date period covers the date passed.

Example usage:
```python
from alldatetime.alldatetime import alldate, alldateperiod
period = alldateperiod(alldate(2023, 12, 1), alldate(2023, 12, 5))
date = alldate(2023, 12, 4)
period.cover(date)  # True
date = alldate(2023, 12, 5)
period.cover(date)  # False
```

### Properties

- `start_date`: The start date of the date period.
- `end_date`: The end date of the date period.

## `Precision`
`Precision` is used to indicate how precise a `fuzzydate` is. It consists of two parts: num and unit.

### Methods and Constructor

#### `__init__(self, num: int, unit: PrecisionUnit)`
- `num`: Required. A number representing precision.
- `unit`: Required. Enum PrecisionUnit: Year, Month, Day.

### Properties

- `num`: A number representing precision.
- `unit`: Enum PrecisionUnit: Year, Month, Day


## `fuzzydate`
`fuzzydate` represents an imprecise time, unlike `alldate` which represents a specific date. `alldate` requires specifying the exact year, month, and day, whereas `fuzzydate` only needs the year specified; the month and day can be left unspecified.

### Methods and Constructor

#### `__init__(self, year: int = None, month: int = None, day: int = None, precision: Precision = None, forward_precision: Precision = None, backward_precision: Precision = None)`
Constructor of class `fuzzydate`.  
- `year`: Required. The year of the fuzzy date. Use negative numbers to represent years before the Common Era (BC).
- `month`: Optional. The month of the fuzzy date.
- `day`: Optional. The day of the fuzzy date.
- `precision`: Optional. The precision of the fuzzy date for both forward and backward.
- `forward_precision`: Optional. The forward precision of the fuzzy date. If not present, precision will be used.
- `backward_precision`: Optional. The forward precision of the fuzzy date. If not present, precision will be used.

Note that, if no precision was passed, `fuzzydate` will infer the precision from the arguments of year, month and day.

#### `to_alldateperiod(self) -> alldateperiod`
Convert the `fuzzydate` to `alldateperiod`.
- **Returns**: An instance of `alldateperiod` representing the range of the `fuzzydate`.

Example usage:
```python
from alldatetime.fuzzydatetime import fuzzydate
fdate = fuzzydate(1987)
fdate.to_alldateperiod() # 1987-01-01 -> 1988-01-01
fdate = fuzzydate(1987, 1)
fdate.to_alldateperiod() # 1987-01-01 -> 1987-01-31
fdate = fuzzydate(1987, 1, 1)
fdate.to_alldateperiod() # 1987-01-01 -> 1987-01-02
```

#### `to_alldateperiod_timestamps(self) -> tuple[float, float]`
Convert the `fuzzydate` to a tuple of two timestamps.
- **Returns**: A tuple of two floats, the first float is the timestamp of start date, and the second float is the timestamp of end date.

Example usage:
```python
from alldatetime.fuzzydatetime import fuzzydate
fdate = fuzzydate(1987)
fdate.to_alldateperiod_timestamps() # 536457600.0 -> 567993600.0
fdate = fuzzydate(1987, 1)
fdate.to_alldateperiod_timestamps() # 536457600.0 -> 539049600.0
fdate = fuzzydate(1987, 1, 1)
fdate.to_alldateperiod_timestamps() # 536457600.0 -> 536544000.0
```

#### `overlap_with(self, other) -> bool`
Check whether the `fuzzydate` overlaps with another `fuzzydate`.
- `other`: An instance of `fuzzydate`.
- **Returns**: Whether the `fuzzydate` overlaps with the `fuzzydate` passed.

Example usage:
```python
from alldatetime.fuzzydatetime import fuzzydate
fdate1, fdate2 = fuzzydate(1987), fuzzydate(1988)
fdate1.overlap_with(fdate2) # False
fdate1, fdate2 = fuzzydate(1987), fuzzydate(1987, 1)
fdate1.overlap_with(fdate2) # True
fdate1, fdate2 = fuzzydate(1987), fuzzydate(1987, 12, 31)
fdate1.overlap_with(fdate2) # True
```

### Properties

- `year`: The year of the fuzzy date.
- `month`: The month of the fuzzy date.
- `day`: The day of the fuzzy date.
- `anchor`: The anchor date of the fuzzy date. It is an instance of `alldate` initiated with the year, month and day. If month or day is absent, 1 is used.
- `forward_precision`: The forward precision.
- `backward_precision`: The backward precision.

## fuzzydateperiod
`fuzzydateperiod` is used to represent a date period, consisting of a fuzzy start date and an fuzzy end date, forming an open-closed interval.

### Methods and Constructor

#### `__init__(self, start_date: fuzzydate, end_date: fuzzydate)`
Constructor of class `fuzzydateperiod`.
- `start_date`: The fuzzy start date of the date period.
- `end_date`: The fuzzy end date of the date period.

#### `cover(self, date: fuzzydate) -> bool`
Check whether the date period covers a fuzzy date.
- `date`: An instance of `fuzzydate`.
- **Returns**: Whether the date period covers the fuzzy date passed.

Example usage:
```python
from alldatetime.fuzzydatetime import fuzzydate, fuzzydateperiod
period = fuzzydateperiod(fuzzydate(202, 1), fuzzydate(202, 5))
period.cover(fuzzydate(202, 3)) # True
period.cover(fuzzydate(202, 1)) # True
period.cover(fuzzydate(202, 6)) # False
```
