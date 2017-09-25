from SerialCommunications import Communicator
from struct import pack


class PowerSource(object):

    def __init__(self,
                 SerialPort=Communicator,
                 address=0x0,
                 current_limit=0,
                 voltage_set=0,
                 alarm_fringe=0,
                ):

        self.SERIAL_PORT = SerialPort

        self.ADDRESS = address
        self.CURRENT_LIMIT = current_limit
        self.VOLTAGE_SET = voltage_set
        self.ALARM_FRINGE = alarm_fringe

        self.ARRAY_TO_SEND = bytearray()

    def set_voltage(self, value):
        is_int = isinstance(value, int)

        if not is_int:
            raise Exception("Please provide integer value for set_voltage() function")

        self.VOLTAGE_SET = value

        if self.VOLTAGE_SET > 20000:
            self.VOLTAGE_SET = 20000

        if self.VOLTAGE_SET < 0:
            self.VOLTAGE_SET = 0

        self.ARRAY_TO_SEND = 'Set Voltage: '.encode() + str(self.VOLTAGE_SET).encode()

        self.SERIAL_PORT.WriteToSerial(self.ARRAY_TO_SEND, self.ADDRESS)

    def set_current(self, value):
        is_int = isinstance(value, int)

        if not is_int:
            raise Exception("Please provide integer value for set_current() function")

        self.CURRENT_LIMIT = value

        if self.CURRENT_LIMIT > 3000:
            self.CURRENT_LIMIT = 3000

        if self.CURRENT_LIMIT < 0:
            self.CURRENT_LIMIT = 0

        self.ARRAY_TO_SEND = 'Set Current: '.encode() + str(self.CURRENT_LIMIT).encode()

        self.SERIAL_PORT.WriteToSerial(self.ARRAY_TO_SEND, self.ADDRESS)