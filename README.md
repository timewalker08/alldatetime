# alldatetime
A lightweight datetime library support year from -100000 to 100000

# Install
    pip install alldatetime

# Usage
## alldate

### Initiate an instance

Initiate an alldate instance by constructor:

    from alldatetime.alldatetime import alldate
    ad = alldate(-1566, 1, 1)
    print(ad.timestamp) # -111553804800

Or initiate an alldate instance from epoch timestamp:

    from alldatetime.alldatetime import alldate
    ad = alldate.fromtimestamp(-111553804800)
    print(ad) # -1566-01-01

## alltime

Initiate an alltime instance by constructor:

    from alldatetime.alldatetime import alltime
    at = alltime(5, 10, 0, 0)

## alldatetime

Initiate an alldatetime instance by constructor:

    from alldatetime.alldatetime import alldatetime
    adt = alldatetime(-1566, 1, 1, 12, 0, 0, 0)
    print(adt.timestamp) # -111553761600

Or initiate an alldate instance from epoch timestamp:

    from alldatetime.alldatetime import alldatetime
    adt = alldatetime.fromtimestamp(-111553761600)
    print(adt) # -1566-01-01 12:00:00
