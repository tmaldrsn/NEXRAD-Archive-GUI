import struct

import numpy as np
from matplotlib import pyplot as plt

from util import unpack, decompress, meta_unpack
import messages


class Volume:
    def __init__(self, filename):
        with open(filename, 'rb') as f:
            raw = f.read()
        
        self.HEADER = unpack(raw[:24], messages.VOLUME_HEADER)
        data = decompress(raw)
        #self.data = data

        # Metadata split according to 2620010G Section 7.3.5 (pg. 7-3)
        # self.METADATA = data[:325888]
        self.TYPE15 = TYPE15(data[:2432*77])
        self.TYPE13 = TYPE13(data[2432*77:2432*126])
        self.TYPE18 = TYPE18(data[2432*126:2432*131])
        self.TYPE3 = TYPE3(data[2432*131:2432*132])
        self.TYPE5 = TYPE5(data[2432*132:2432*133])
        self.TYPE2 = TYPE2(data[2432*133:2432*134])
        
        self.STATUS_MESSAGES = []
        self.RADAR_DATA = []

        pointer = 325888
        while True:
            if pointer >= len(data):
                break

            try:
                message_len = struct.unpack('>H', data[pointer+12:pointer+14])[0]*2 + 12
                message_type = data[pointer+15]
                
                ##############################################################
                # Dealing with embedded Type 2 Messages outside of metadata  #
                ##############################################################
                # Following the Metadata Record is a variable number of      #
                # compressed records containing 120 radial messages(type 31) #
                # plus 0 or more RDA Status messages(type 2).                #
                #                                                            #
                # SOURCE: 2620010G pg. 7-3 #                                 #
                ##############################################################
                if message_type == 2:
                    self.STATUS_MESSAGES.append(Message(data[pointer:pointer+2432]))
                    pointer += 2432
                    continue

                self.RADAR_DATA.append(TYPE31(data[pointer:pointer+message_len])) 
                pointer += message_len
                
            except IndexError as e:
                raise e
    
    def elevation_data(self, elevation=1, moment='DREF'):
        theta, r, z = [], [], []
        for mess in [i for i in self.RADAR_DATA if i._elevation==elevation]:
            theta.append(mess.get_radar_data(moment)[0])
            r.append(mess.get_radar_data(moment)[1])
            z.append(mess.get_radar_data(moment)[2])

        return np.array(theta), np.array(r), np.ma.masked_where(np.equal(z, 0), z)

    def available_scans(self):
        return {mess._elevation: mess.get_available_scans() for mess in self.RADAR_DATA}

    def num_elevations(self):
        return max(self.available_scans().keys())


class MessageHeader:
    def __init__(self, buffer, parentMessage=None):
        self.parentMessage = parentMessage
        self.data = unpack(buffer, messages.MESSAGE_HEADER)


class Message:
    def __init__(self, buffer):
        assert buffer[:12] == bytes(12)
        self.header = MessageHeader(buffer[12:28], self) # message size includes header
        self.data = buffer[28:]

    def __len__(self):
        return self.header.data["Message Size"]*2-16


class ExtendedMessage:
    def __init__(self, buffer):
        self.headers = []
        self.buffer = b''

        pointer = 0
        while True:
            if pointer >= len(buffer) or buffer[pointer+12:pointer+28] == bytes(16):
                #self.buffer = self.buffer.rstrip(b'\x00')
                break
            message = Message(buffer[pointer:pointer+2432])
            self.headers.append(message.header)
            self.buffer += message.data
            pointer += 2432

    def __len__(self):
        return sum([h.data["Message Size"]*2-16 for h in self.headers])

class TYPE2(Message):
    def __init__(self, buffer):
        Message.__init__(self, buffer)
        self.unpacked_data = meta_unpack(self.data[:len(self)-40-28], messages.TYPE2)
        delattr(self, 'data')
        

class TYPE3(Message):
    def __init__(self, buffer):
        Message.__init__(self, buffer)
        self.unpacked_data = meta_unpack(self.data[:958], messages.TYPE3)
        delattr(self, 'data')

class TYPE5(Message):
    def __init__(self, buffer):
        Message.__init__(self, buffer)
        self.unpacked_data = meta_unpack(self.data[:67], messages.TYPE5)
        delattr(self, 'data')

class TYPE13(ExtendedMessage):
    def __init__(self, buffer):
        ExtendedMessage.__init__(self, buffer)
        self.unpacked_data = meta_unpack(self.buffer[:6], messages.TYPE13_HEAD)
        delattr(self, 'buffer')


class TYPE15(ExtendedMessage):
    def __init__(self, buffer):
        ExtendedMessage.__init__(self, buffer)
        self.unpacked_data = meta_unpack(self.buffer[:6], messages.TYPE15_HEAD)
        delattr(self, 'buffer')


class TYPE18(ExtendedMessage):
    def __init__(self, buffer):
        ExtendedMessage.__init__(self, buffer)
        self.unpacked_data = meta_unpack(self.buffer[:len(self)], messages.TYPE18)
        delattr(self, 'buffer')


class TYPE31(Message):
    def __init__(self, buffer):
        Message.__init__(self, buffer)
        
        #self.DATA_HEADER = unpack(self.data[:68], messages.TYPE31_HEADER)
        #self.RVOL = unpack(self.data[68:68+44], messages.TYPE31_RVOL)
        #self.RELV = unpack(self.data[112:112+12], messages.TYPE31_RELV)
        #self.RRAD = unpack(self.data[124:124+28], messages.TYPE31_RRAD)

        self.DREF = self.get_data_block('DREF')
        self.DVEL = self.get_data_block('DVEL')
        self.DSW = self.get_data_block('DSW')
        self.DZDR = self.get_data_block('DZDR')
        self.DPHI = self.get_data_block('DPHI')
        self.DRHO = self.get_data_block('DRHO')

        DATA_HEADER = unpack(self.data[:68], messages.TYPE31_HEADER)
        RVOL = unpack(self.data[68:68+44], messages.TYPE31_RVOL)
        #RELV = unpack(self.data[112:112+12], TYPE31_RELV)

        self._elevation = DATA_HEADER['Elevation Number']
        self._azimuth_number = DATA_HEADER['Azimuth Number']
        self._azimuth_angle = DATA_HEADER['Azimuth Angle']
        self._coords = [RVOL['Latitude'], RVOL['Longitude']]


    def get_data_block(self, moment):
        data_loc = self.data.find(bytes(moment, 'utf-8'))
        if data_loc == -1:
            return
        
        data_info = unpack(self.data[data_loc:data_loc+28], messages.TYPE31_DATA)
        data_moment = data_info['Data Block Type'] + data_info['Data Moment Name'] 
        word_size = data_info['Data Word Size'] // 8
        data_len = data_info['Number of Data Moment Gates']
        conv = lambda x: (x - data_info['Offset']) / data_info['Scale'] if x else 0
        
        bad_data = []

        if word_size == 1:
            char = 'B'
        else:
            char = 'H'

        try:
            radar_data = struct.unpack('>' + char*data_len, self.data[data_loc:data_loc+data_len*word_size])
            data_info['DATA'] = list(map(conv, list(radar_data)))[28:]
        except struct.error:
            bad_data.append(data_info)
            print('bad data... {}'.format(data_moment))
            print(data_info)

        return data_info

    def get_radar_data(self, moment):
        moment_data = self.__dict__.get(moment)
        if not moment_data:
            return

        z = moment_data['DATA']
        r_init = moment_data['Data Moment Range']
        r_step = moment_data['Data Moment Range Sample Interval']
        r = [r_init+r_step*i for i in range(len(z))]

        to_rad = lambda x: 2*np.pi*x / 360
        theta = list(map(to_rad, [self._azimuth_angle for i in range(len(z))]))

        return [theta, r, z]

    def get_available_scans(self):
        messages = {
            'DREF': self.DREF,
            'DVEL': self.DVEL,
            'DSW': self.DSW,
            'DZDR': self.DZDR,
            'DPHI': self.DPHI,
            'DRHO': self.DRHO
        }
        return [mess for mess in messages.keys() if messages[mess]]

# debug purposes
if __name__=='__main__':
    vol = Volume('raw/KFDX20190712_042038_V06')
    fig = vol.elevation_data()
