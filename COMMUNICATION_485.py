from PyCRC.CRC16 import CRC16
from PyCRC.CRCCCITT import CRCCCITT
from struct import pack, unpack

class data_packet(object):
    ADDR=0x00
    DTA=''
    CRC=0x00

BIN=bytearray()

def calc_crc(self):
    self.CRC=CRCCCITT().calculate(self.DTA)

def print_data(self):
    print('Мой адресс:',self.ADDR)
    print('Мои данные:',self.DTA)
    print('Размер данных',len(self.DTA))
    print('Мой CRC16:',hex(self.CRC))
    nl=0
    for x in self.BIN:
        print(hex(x),end='\t')
        nl=nl+1
        if nl==5:
           print('')
        nl=0

def pack_to_bin(self):
    self.BIN=pack('B',self.ADDR)
    sz=len(self.DTA)
    self.BIN=self.BIN+pack('B',sz)
    self.BIN=self.BIN+self.DTA.encode()
    self.BIN=self.BIN+pack('H',self.CRC)

pack0=data_packet()

pack0.ADDR=0x5
pack0.DTA=b'OLEG'.decode()
pack0.calc_crc()
pack0.pack_to_bin()

pack0.print_data()