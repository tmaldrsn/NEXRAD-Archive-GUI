import pytest
import struct
import messages

def test_message_type2_has_correct_format_length():
    fmt = ''.join([item[1] for item in messages.TYPE2])
    assert struct.calcsize(fmt) == 120

def test_message_type3_has_correct_format_length():
    fmt = ''.join([item[1] for item in messages.TYPE3])
    assert struct.calcsize(fmt) == 960

def test_message_type5head_has_correct_format_length():
    fmt = ''.join([item[1] for item in messages.TYPE5_HEAD])
    assert struct.calcsize(fmt) == 22

def test_message_type5elev_has_correct_format_length():
    fmt = ''.join([item[1] for item in messages.TYPE5_ELEV])
    assert struct.calcsize(fmt) == 46

def test_message_type13head_has_correct_format_length():
    fmt = ''.join([item[1] for item in messages.TYPE13_HEAD])
    assert struct.calcsize(fmt) == 6

def test_message_type15head_has_correct_format_length():
    fmt = ''.join([item[1] for item in messages.TYPE15_HEAD])
    assert struct.calcsize(fmt) == 6
    
def test_message_type15rz_has_correct_format_length():
    fmt = ''.join([item[1] for item in messages.TYPE15_RZ])
    assert struct.calcsize(fmt) == 4

def test_message_type18_has_correct_format_length():
    fmt = ''.join([item[1] for item in messages.TYPE18])
    # see line 828 for the error in type18 alignment
    # `errored` assert bc of dumb documentation:
    assert struct.calcsize(fmt) == 9468 - 12

def test_message_type31head_has_correct_format_length():
    fmt = ''.join([item[1] for item in messages.TYPE31_HEADER])
    assert struct.calcsize(fmt) == 68

def test_message_type31rvol_has_correct_format_length():
    fmt = ''.join([item[1] for item in messages.TYPE31_RVOL])
    assert struct.calcsize(fmt) == 44

def test_message_type31relv_has_correct_format_lengtH():
    fmt = ''.join([item[1] for item in messages.TYPE31_RELV])
    assert struct.calcsize(fmt) == 12

def test_message_type31rrad_has_correct_format_length():
    fmt = ''.join([item[1] for item in messages.TYPE31_RRAD])
    assert struct.calcsize(fmt) == 28

def test_message_type31data_has_correct_format_length():
    fmt = ''.join([item[1] for item in messages.TYPE31_DATA])
    assert struct.calcsize(fmt) == 28
