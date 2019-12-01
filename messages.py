from util import datetime_from_julian, time_from_milliseconds, scale

# Document 2620010G - Section 7.3.3 (pg. 13)
VOLUME_HEADER = (
    ('Tape Filename', '9s', None, bytes.decode),
    ('Extension Number', '3s', None, bytes.decode),
    ('Date', 'L', None, datetime_from_julian),
    ('Time', 'L', None, time_from_milliseconds),
    ('ICAO', '4s', None, bytes.decode)
)

# Document 2620002R - Section 3.2.4.1 Table II (pgs. 3-6 to 3-7)
MESSAGE_HEADER = (
    ('Message Size', 'H', 'halfwords', None),
    ('RDA Redundant Channel', 'B', None, None),
    ('Message Type', 'B', None, None),
    ('I.D. Sequence Number', 'H', None, None),
    ('Date', 'H', None, datetime_from_julian),
    ('Time', 'L', None, time_from_milliseconds),
    ('Number of Message Segments', 'H', None, None),
    ('Message Segment Number', 'H', None, None)
)

###############################################
# TYPE 31 - DIGITAL RADAR DATA GENERIC FORMAT #
###############################################
# Document 2620002R - Section 3.2.4.17.1 Table XVII-A (pg. 3-89 to 3-91)
TYPE31_HEADER = (
    ('Radar Identifier', '4s', None, None),
    ('Collection Time', 'L', None, time_from_milliseconds),
    ('Collection Date', 'H', None, datetime_from_julian),
    ('Azimuth Number', 'H', None, None),
    ('Azimuth Angle', 'f', 'deg', None),
    ('Compression Indicator', 'B', None, None),
    # (None, 'x', None, None)
    (None, 'B', None, None),
    ('Radial Length', 'H', None, None),
    ('Azimuth Resolution Spacing', 'B', None, None),
    ('Radial Status', 'B', None, None),
    ('Elevation Number', 'B', None, None),
    ('Cut Sector Number', 'B', None, None),
    ('Elevation Angle', 'f', 'deg', None),
    ('Radial Spot Blanking Status', 'B', None, None),
    ('Azimuith Indexing Mode', 'B', None, scale(0.01)),
    ('Data Block Count', 'H', None, None),
    ('Block 1 Pointer', 'L', None, None),
    ('Block 2 Pointer', 'L', None, None),
    ('Block 3 Pointer', 'L', None, None),
    ('Block 4 Pointer', 'L', None, None),
    ('Block 5 Pointer', 'L', None, None),
    ('Block 6 Pointer', 'L', None, None),
    ('Block 7 Pointer', 'L', None, None),
    ('Block 8 Pointer', 'L', None, None),
    ('Block 9 Pointer', 'L', None, None),
)

# Document 2620002R - Section 3.2.4.17.2 Table XVII-B (pgs. 3-91 to 3-93)
TYPE31_DATA = (
    ('Data Block Type', '1s', None, None),
    ('Data Moment Name', '3s', None, None),
    # (None, 'xxxx', None, None)
    (None, 'L', None, None),
    ('Number of Data Moment Gates', 'H', None, None),
    ('Data Moment Range', 'H', 'km', scale(0.001)),
    ('Data Moment Range Sample Interval', 'H', 'km', scale(0.001)),
    ('TOVER', 'H', 'dB', scale(0.1)),
    ('SNR Threshold', 'h', 'dB', scale(0.125)),
    ('Control Flags', 'B', None, None),
    ('Data Word Size', 'B', None, None),
    ('Scale', 'f', None, None),
    ('Offset', 'f', None, None),
)

# Document 2620002R - Section 3.2.4.17.3 Table XVII-E (pgs. 3-93 to 3-94)
TYPE31_RVOL = (
    ('Data Block Type', '1s', None, None),
    ('Data Name', '3s', None, None),
    ('Data Block Size', 'H', None, None),
    ('Version Number (Major)', 'B', None, None),
    ('Version Number (Minor)', 'B', None, None),
    ('Latitude', 'f', 'deg', None),
    ('Longitude', 'f', 'deg', None),
    ('Site Height', 'h', 'm', None),
    ('Feedhorn Height', 'H', 'm', None),
    ('Calibration Constant (dbZ0)', 'f', 'dB', None),
    ('Horizontal SHV Tx Power', 'f', 'kW', None),
    ('Vertical SHV Tx Power', 'f', 'kW', None),
    ('System Differential Reflectivity', 'f', 'dB', None),
    ('Initial System Differential Phase', 'f', 'deg', None),
    ('Volume Coverage Pattern Number', 'H', None, None),
    ('Processing Status', 'H', None, None)
)

# Document 2620002R - Section 3.2.4.17.4 Table XVII-F (pg. 3-94)
TYPE31_RELV = (
    ('Data Block Type', '1s', None, None),
    ('Data Name', '3s', None, None),
    ('Data Block Size', 'H', None, None),
    ('ATMOS', 'h', 'dB/km', scale(0.001)),
    ('Calibration Constant (dbZ0)', 'f', 'dB', None)
)

# Document 2620002R - Section 3.2.4.17.5 Table XVII-H (pg.3-94 to 3-95)
TYPE31_RRAD = (
    ('Data Block Type', '1s', None, None),
    ('Data Name', '3s', None, None),
    ('Data Block Size', 'H', None, None),
    ('Unambiguous Range', 'H', 'km', scale(0.1)),
    ('Noise Level (Horizontal Channel)', 'f', 'dBm', None),
    ('Noise Level (Vertical Channel)', 'f', 'dBm', None),
    ('Nyquist Velocity', 'H', 'm/s', scale(0.01)),
    (None, 'xx', None, None),
    ('Calibration Constant (Horizontal Channel)', 'f', 'dBZ', None),
    ('Calibration Constant (Vertical Channel)', 'f', 'dBZ', None)
)
