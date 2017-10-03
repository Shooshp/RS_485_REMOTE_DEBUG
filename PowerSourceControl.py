import struct
import traceback

class PowerSource(object):

    command_set_voltage      = 1
    command_set_current      = 2
    command_set_alarm_fringe = 3
    command_read_voltage     = 4
    command_read_current     = 5
    command_read_temperature = 6
    command_control_turn_on  = 7
    command_control_turn_off = 8

    def __init__(self,
                 serial_port,
                 address=0x0,
                 current_limit=0,
                 voltage_set=0,
                 alarm_fringe=0,
                 def_name = None
                 ):

        self.SERIAL_PORT = serial_port

        self.ADDRESS = address
        self.CURRENT_LIMIT = current_limit
        self.VOLTAGE_SET = voltage_set
        self.ALARM_FRINGE = alarm_fringe

        self.ARRAY_TO_SEND = bytearray()
        self.OBJECT_TYPE = __class__.__name__

        if def_name == None:
            (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
            def_name = text[:text.find('=')].strip()
        self.defined_name = def_name

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

        self.SERIAL_PORT.write_to_serial(
            command = self.command_set_voltage,
            data    = self.ARRAY_TO_SEND,
            address = self.ADDRESS,
            instance_name= self.defined_name,
            object_type= self.OBJECT_TYPE
            )

    def set_current(self, value):
        is_int = isinstance(value, int)

        if not is_int:
            raise Exception("Please provide integer value for set_current() function")

        self.CURRENT_LIMIT = value

        if self.CURRENT_LIMIT > 3000:
            self.CURRENT_LIMIT = 3000

        if self.CURRENT_LIMIT < 0:
            self.CURRENT_LIMIT = 0

        self.ARRAY_TO_SEND = struct.pack('>H', self.CURRENT_LIMIT)

        self.SERIAL_PORT.write_to_serial(
            command=self.command_set_current,
            data=self.ARRAY_TO_SEND,
            address=self.ADDRESS,
            instance_name=self.defined_name,
            object_type=self.OBJECT_TYPE
        )
