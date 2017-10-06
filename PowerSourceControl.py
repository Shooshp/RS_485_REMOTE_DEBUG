import struct
import traceback
from HostController import HostController
from AVR import Atmega16RegisterMap as Atmega16
from enum import IntEnum


class PowerSourceCommands(IntEnum):
    set_voltage = 1
    set_current = 2
    set_alarm_fringe = 3
    read_voltage = 4
    read_current = 5
    read_temperature = 6
    turn_on = 7
    turn_off = 8

    register_write = 20
    register_read = 21


class PowerSource(HostController):
    def __init__(self, address):

        super().__init__(address=address)
        if self.INSTANCE_NAME is None:
            (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
            self.INSTANCE_NAME = text[:text.find('=')].strip()

        if self.OBJECT_TYPE is None:
            self.OBJECT_TYPE = __class__.__name__

        self.CURRENT_LIMIT = 0
        self.VOLTAGE_SET = 0

    def set_voltage(self, value):
        is_int = isinstance(value, int)

        if not is_int:
            raise Exception("Please provide integer value for set_voltage() function")

        self.VOLTAGE_SET = value

        if self.VOLTAGE_SET > 20000:
            self.VOLTAGE_SET = 20000

        if self.VOLTAGE_SET < 0:
            self.VOLTAGE_SET = 0

        self.ARRAY_TO_SEND = struct.pack('>H', self.VOLTAGE_SET)
        self.COMMAND = PowerSourceCommands.set_voltage
        self.write(self)

    def set_current(self, value):
        is_int = isinstance(value, int)

        if not is_int:
            raise Exception("Please provide integer value for set_current() function")

        if self.CURRENT_LIMIT > 3000:
            self.CURRENT_LIMIT = 3000

        if self.CURRENT_LIMIT < 0:
            self.CURRENT_LIMIT = 0

        self.ARRAY_TO_SEND = struct.pack('>H', self.CURRENT_LIMIT)
        self.COMMAND = PowerSourceCommands.set_current
        self.write(self)

    def write_to_register(self, address, value):
        self.ARRAY_TO_SEND = struct.pack('>HB', address, value)
        self.COMMAND = PowerSourceCommands.register_write
        self.write()

    def read_from_register(self, address):
        self.ARRAY_TO_SEND = struct.pack('>H', address)
        self.COMMAND = PowerSourceCommands.register_read
        data = self.read(self)
        return data



class AVR_SPI(object):
    spi_port = Atmega16.PORTB
    spi_ddr  = Atmega16.DDRB
    spi_ddr_MISO = Atmega16.DDB6
    spi_ddr_MOSI = Atmega16.DDB5
    spi_ddr_SS   = Atmega16.DDB4
    spi_ddr_CLK  = Atmega16.DDB7
    spi_pin_SS = Atmega16.PINB4

    data_read = bytes
    data_write = bytes

    def SPI_SELECT(self):
        data_read = PowerSource.read_from_register(self.spi_port)
