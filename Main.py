from AVR import Atmega16RegisterMap as AVR
from PowerSourceControl import PowerSource
from SerialCommunications import Communicator

Communicator.open_port()

VCC_INT = PowerSource(address=0xAA)
VCC_LOAD = PowerSource(address=0xA3)



VCC_INT.write_to_register(AVR.DDRA, 0xFF)

counter = 0
while counter < 10:
    #VCC_INT.set_voltage(1500)
    #VCC_LOAD.set_current(3200)
    VCC_INT.write_to_register(AVR.PORTA,0x00)
    VCC_INT.write_to_register(AVR.PORTA,0xFF)

    counter +=1

VCC_INT.write_to_register(AVR.DDRA, 0x00)


