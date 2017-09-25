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



        self.BIN = 'Address: '.encode() + pack('B', self.ADDR) + '\n\r'.encode()
        self.BIN = self.BIN + 'Length: '.encode() + pack('B', len(data)) + '\n\r'.encode()
        self.BIN = self.BIN + data + '\n\r'.encode()
        self.BIN = self.BIN + 'CRC: '.encode() + pack('H', CRC16().calculate(self.BIN)) + '\n\r'.encode()

        print(self.BIN)

        return self.BIN
