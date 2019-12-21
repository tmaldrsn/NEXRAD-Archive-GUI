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

def test_angle_data_msb_only_gives_180():
    assert angle_data(b'\x80\x00') == 180.

def test_angle_data_with_bits_0_thru_2_only_returns_0():
    assert angle_data(b'\x00\x07') == 0.

def test_range_data_msb_is_0_returns_positive():
    assert range_data(b'\xc0\x00') == -16.384

def test_range_data_msb_is_1_returns_negative():
    assert range_data(b'\x40\x00') == 16.384

def test_range_data_lsb_returns_1_meter():
    assert range_data(b'\x00\x01') == 0.001 # 0.001km = 1m