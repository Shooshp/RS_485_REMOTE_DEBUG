from PyCRC.CRC16 import CRC16
from struct import pack

class data_packet(object):

    DTA = ''
    CRC = 0x00

    BIN = bytearray()

    def __init__(self,
                 addr = 0x0,
                 crc_constant = 0xA001):

        self.ADDR = addr
        self.CRC_CONSTANT = crc_constant

    def pack_data(self, data):
        is_string = isinstance(data, str)
        is_bytes = isinstance(data, bytes)

        if not is_string and not is_bytes:
            raise Exception("Please provide a string or a byte sequence as argument for calculation.")

        CRC16().crc16_constant = self.CRC_CONSTANT

        self.CRC = CRC16().calculate(data)

        self.BIN = pack('B', self.ADDR)
        self.BIN = self.BIN+pack('B', len(self.DTA))
        self.BIN = self.BIN + self.DTA.encode()
        self.BIN = self.BIN + pack('H', self.CRC)

        return self.BIN
