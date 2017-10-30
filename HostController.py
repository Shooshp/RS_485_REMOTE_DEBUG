from enum import IntEnum

class DevicePrefixes(IntEnum):
    PowerSource = 0xA0
    Commutator = 0xB0
    FPGA = 0xC0
    ControlPanel = 0xD0

class HostController(object):

    def __init__(self,
                 address=None,
                 communicator=None,
                 ):

        self.COMMUNICATOR = communicator
        self.ADDRESS = address
        self.DEVICE_ADDRESS_PREFIX = None
        self.ARRAY_TO_SEND = bytearray()
        self.ARRAY_TO_RECEIVE = bytearray()
        self.COMMAND = bytes()

        self.INSTANCE_NAME = None
        self.OBJECT_TYPE = None
        self.DEVICE_ID = bytearray()

    def write(self):
        self.COMMUNICATOR.write_to_serial(self)

    def read(self):
        self.COMMUNICATOR.read_from_serial(self)
