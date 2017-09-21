from PyCRC.CRC16 import CRC16
from struct import pack

class data_packet(object):

    def __init__(self,
                 addr = 0x0,
                 crc_constant = 0xA001):

        self.ADDR = addr
        self.CRC_CONSTANT = crc_constant
        self.BIN = bytearray()

    def pack_data(self, data):
        is_string = isinstance(data, str)
        is_bytes = isinstance(data, bytes)

        if not is_string and not is_bytes:
            raise Exception("Please provide a string or a byte sequence as argument for calculation.")

        CRC16().crc16_constant = self.CRC_CONSTANT

        self.CRC = CRC16().calculate(data)

        self.BIN = 'Address: '.encode() + pack('B', self.ADDR)
        self.BIN = self.BIN + 'Length: '.encode() + pack('B', len(data))
        self.BIN = self.BIN + data
        self.BIN = self.BIN + 'CRC: '.encode() + pack('H', self.CRC)

        print(self.BIN)

        return self.BIN
