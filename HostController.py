import  SerialCommunications

class HostController(object):

    def __init__(self, address = None):

        self.ADDRESS = address
        self.INSTANCE_NAME = None
        self.OBJECT_TYPE = None

        self.ARRAY_TO_SEND = bytearray()
        self.ARRAY_TO_RECEIVE = bytearray()
        self.COMMAND = bytes()


    def write(self, host):
        SerialCommunications.Communicator.write_to_serial(host)

    def read(self, host):
        SerialCommunications.Communicator.read_from_serial(host)

