import struct
import traceback
from HostController import HostController
from enum import IntEnum

class PowerSourceCommands(IntEnum):
    set_voltage      = 1
    set_current      = 2
    set_alarm_fringe = 3
    read_voltage     = 4
    read_current     = 5
    read_temperature = 6
    turn_on          = 7
    turn_off         = 8

class PowerSource(HostController):

    def __init__(self, address):

        super().__init__(address = address)
        if self.INSTANCE_NAME is None:
            (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
            self.INSTANCE_NAME = text[:text.find('=')].strip()

        if self.OBJECT_TYPE is None:
            self.OBJECT_TYPE = __class__.__name__

        self.CURRENT_LIMIT = 0
        self.VOLTAGE_SET   = 0


    def set_voltage(self, value):
        is_int = isinstance(value, int)

        if not is_int:
            raise Exception("Please provide integer value for set_voltage() function")

        self.VOLTAGE_SET = value

        if self.VOLTAGE_SET > 20000:
            self.VOLTAGE_SET = 20000

        if self.VOLTAGE_SET < 0:
            self.VOLTAGE_SET = 0

        self.ARRAY_TO_SEND = struct.pack('>H',self.VOLTAGE_SET)
        self.COMMAND = PowerSourceCommands.set_voltage
        self.write(self)

        #self.SERIAL_PORT.write_to_serial(
        #    command = PowerSourceCommands.command_set_voltage,
        #   data    = self.ARRAY_TO_SEND,
        #   address = self.ADDRESS,
        #   instance_name= self.defined_name,
        #   object_type= self.OBJECT_TYPE
        #    )

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

       # self.SERIAL_PORT.write_to_serial(
        #    command=PowerSourceCommands.set_current,
        #    data=self.ARRAY_TO_SEND,
        #    address=self.ADDRESS,
        #    instance_name=self.defined_name,
        #    object_type=self.OBJECT_TYPE
        #)



