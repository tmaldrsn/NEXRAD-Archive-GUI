import matplotlib as mpl

def get_cmap(d):
    bounds = list(d.keys())
    colors = list(d.values())

    cmap = mpl.colors.ListedColormap(colors)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    return cmap, norm

def get_colordict(moment):
    if moment == 'DREF':
        return REF_PRECIP_16
    elif moment == 'DVEL':
        return VEL_16
    elif moment == 'DSW':
        return DSW_8
    elif moment == 'DZDR':
        return ZDR_16
    elif moment == 'DPHI':
        return KDP_16
    elif moment == 'DRHO':
        return DCC_16

############################
# RADAR COLORBAR CONSTANTS #
############################
"""
    Color codes come in 8 or 16, and are represented by a hex value
    between 0 and 8 or 15. Each of the codes are also represented by
    a value range. Currently I'm using the value ranges as the dictionary
    keys instead of the 0-8 or 0-15 codes to avoid multiple conversions
"""

# REFLECTIVITY
REF_8 = {
    #'ND': '#000000',
    5: '#FFAAAA',
    18: '#C97070',
    30: '#00BB00',
    41: '#FFFF70',
    46: '#DA0000',
    50: '#0000FF',
    57: '#FFFFFF'
}

REF_PRECIP_16 = {
    #'ND': '#000000',
    5: '#9C9C9C',
    10: '#767676',
    15: '#FFAAAA',
    20: '#EE8C8C',
    25: '#C97070',
    30: '#00FB90',
    35: '#00BB00',
    40: '#FFFF70',
    45: '#D0D060',
    50: '#FF6060',
    55: '#DA0000',
    60: '#AE0000',
    65: '#0000FF',
    70: '#FFFFFF',
    75: '#E700FF'
}

REF_CLEAR_16 = {
    #'ND': '#000000',
    -28: '#9C9C9C',
    -24: '#767676',
    -20: '#FFAAAA',
    -16: '#EE8C8C',
    -12: '#C97070',
    -8: '#00FB90',
    -4: '#00BB00',
    0: '#FFFF70',
    4: '#D0D060',
    8: '#FF6060',
    12: '#DA0000',
    16: '#AE0000',
    20: '#0000FF',
    24: '#FFFFFF',
    28: '#E700FF'
}

#VELOCITY
VEL_8 = {
    #'ND': '#000000',
    -10: '#00E0FF',
    -5: '#00BB00',
    -1: '#008F00',
    0: '#F88700',
    5: '#FFCF00',
    10: '#FF0000',
    #'RF': '#77007D
}

VEL_16 = {
    #'ND': '#000000',
    -64: '#00E0FF',
    -50: '#0080FF',
    -36: '#320096',
    -26: '#00FB90',
    -20: '#00BB99',
    -10: '#008F00',
    -1: '#CDC99F',
    0: '#767676',
    10: '#F88700',
    20: '#FFCF00',
    26: '#FFFF00',
    36: '#AE0000',
    50: '#D07000',
    64: '#FF0000',
    #'RF': '#77007D
}

# SPECTRUM WIDTH
DSW_8 = {
    #'ND': '#000000',
    0: '#767676',
    4: '#9C9C9C',
    8: '#00BB00',
    12: '#FF0000',
    16: '#D07000',
    20: '#FFFF00',
    #'RF': '#77007D'
}

# DIFFERENTIAL REFLECTIVITY
ZDR_16 = {
    #'ND': '#000000',
    -4.0: '#404040',
    -2.0: '#9C9C9C',
    -0.5: '#C9C9C9',
    0.0: '#8C78B4',
    0.25: '#000098',
    0.5: '#2398D3',
    1.0: '#44FFD2',
    1.5: '#57DB56',
    2.0: '#FFFF60',
    2.5: '#FF9045',
    3.0: '#DA0000',
    4.0: '#AE0000',
    5.0: '#F782BE',
    6.0: '#FFFFFF',
    #'RF': '#77007D'
}

# CORRELATION COEFFICIENT
DCC_16 = {
    #'ND': '#000000',
    0.20: '#95949C',
    0.45: '#16148C',
    0.65: '#0902D9',
    0.75: '#8987D6',
    0.80: '#5CFF59',
    0.85: '#8BCF02',
    0.90: '#FFFB00',
    0.93: '#FFC400',
    0.95: '#FF8903',
    0.96: '#FF2B00',
    0.97: '#E30000',
    0.98: '#A10000',
    0.99: '#970556',
    1.00: '#FAACD1',
    #'RF': '#77007D',
}

# DIFFERENTIAL PHASE
KDP_16 = {
    #'ND': '#000000',
    -2.0: '#767676',
    -1.0: '#4B4B4B',
    -0.5: '#4B0000',
    0.0: '#730019',
    0.25: '#A5082C',
    0.5: '#D5475C',
    1.0: '#EB78B9',
    1.5: '#9681B7',
    2.0: '#62FFFA',
    2.5: '#14B932',
    3.0: '#0AFF0A',
    4.0: '#FFFF00',
    5.0: '#FF7814',
    7.0: '#FFCD82',
    #'RF': '#77007D'
}

bounds = {
    'DREF': [-32.0, 94.5],
    'DVEL': [-63.5, 63.0],
    'DSW': [-63.5, 63.0],
    'DZDR': [-7.8750, 7.9375],
    'DPHI': [0, 360],
    'DRHO': [0.2083, 1.0516]
}