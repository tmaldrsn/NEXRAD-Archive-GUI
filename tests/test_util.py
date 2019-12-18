import pytest
import datetime
from util import (
    datetime_from_julian,
    time_from_milliseconds,
    time_from_minutes,
    scale,
    angle_data,
    range_data
)

def test_julian_date_one_is_correct():
    assert datetime_from_julian(1) == datetime.date(1970, 1, 1)

def test_time_after_zero_milliseconds_is_midnight():
    assert time_from_milliseconds(0) == datetime.time(0, 0, 0)

def test_time_after_zero_minutes_is_midnight():
    assert time_from_minutes(0) == datetime.time(0, 0, 0)
