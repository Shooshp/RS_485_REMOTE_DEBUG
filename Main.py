from AVR import Atmega16RegisterMap as AVR
from PowerSourceControl import PowerSource
from SerialCommunications import Communicator


RS485 = Communicator()

VCC_INT = PowerSource(address=0xAA, communicator= RS485)


#VCC_INT.clear_device_id()




