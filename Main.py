from AVR import Atmega16RegisterMap as AVR
from PowerSourceControl import PowerSource
#from SerialCommunications import Communicator

#Communicator.open_port()

VCC_INT = PowerSource(address=0xAA)
VCC_LOAD = PowerSource(address=0xA3)




