import datetime
import struct
import bz2


def datetime_from_julian(julian_date):
    day_one = datetime.date(1970, 1, 1)
    return day_one + datetime.timedelta(days=julian_date-1)


def time_from_milliseconds(millis):
    init_time = datetime.datetime(1970, 1, 1, 0, 0, 0)
    return (init_time + datetime.timedelta(microseconds=millis*1000)).time()


def time_from_minutes(minutes):
    init_time = datetime.datetime(1970, 1, 1, 0, 0, 0)
    return (init_time + datetime.timedelta(minutes=minutes)).time()


def scale(factor):
    return lambda x: x*factor


# 2620002R Table III-A, pg. 3-11
def angle_data(b):
    bits = format(int(b.hex(), 16), '016b')
    return sum([180/2**i for i, bit in enumerate(bits[:-3]) if int(bit)])

# 2620002R Table III-B, pg. 3-11 to 3-12
def range_data(b):
    bits = format(int(b.hex(), 16), '016b')
    sign = (-1) ** int(bits[0])
    return sign * sum([16.384 / 2**i for i, bit in enumerate(bits[1:]) if int(bit)])

def meta_unpack(buffer, fmt):
    info = struct.unpack('>' + ''.join([item[1] for item in fmt]), buffer)
    info_dict = {}
    offset = 0
    for i in range(len(fmt)):
        key = fmt[i][0]
        if not key:
            offset += 1
            continue
        if fmt[i][3] is not None:
            try:
                info_dict[key] = fmt[i][3](info[i-offset])
            except TypeError:
                print(fmt[i])
                print(info[i-offset])
        else:
            info_dict[key] = info[i-offset]

    return info_dict


def unpack(buffer, fmt):
    info = struct.unpack('>'+''.join([item[1] for item in fmt]), buffer)
    info_dict = {}
    for i in range(len(fmt)):
        key = fmt[i][0]
        if not key:
            continue
        if fmt[i][3] is None:
            info_dict[key] = info[i]
        else:
            info_dict[key] = fmt[i][3](info[i])
    return info_dict

def decompress(buffer):
    pointer = 24
    decompressed = b""
    while pointer < len(buffer):
        compressed_len = struct.unpack('>I', buffer[pointer:pointer+4])[0]
        pointer += 4
        dc = bz2.BZ2Decompressor()

        # check to make sure pointer is in the correct place
        assert buffer[pointer:pointer+10] == b'BZh91AY&SY'

        try:
            decompressed += dc.decompress(buffer[pointer:])
        except:
            raise Exception("Something went wrong at byte #{}".format(pointer))

        pointer += compressed_len

    return decompressed
