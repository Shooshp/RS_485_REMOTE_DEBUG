# from SerialCommunications import Communicator


class HostController(object):
    def __init__(self, address=None):
        self.ADDRESS = address
        self.ARRAY_TO_SEND = bytearray()
        self.ARRAY_TO_RECEIVE = bytearray()
        self.COMMAND = bytes()

        self.INSTANCE_NAME = None
        self.OBJECT_TYPE = None

    def write(self):
        Communicator.write_to_serial(
            address=self.ADDRESS,
            command=self.COMMAND,
            data=self.ARRAY_TO_SEND,
            name=self.INSTANCE_NAME,
            type=self.OBJECT_TYPE)

