from AVR import Atmega16RegisterMap as AVR
from PowerSourceControl import PowerSource
from SerialCommunications import Communicator
import time

RS485 = Communicator()

VCC_INT = PowerSource(address=0xAA, communicator= RS485)



for i in range (0, 2560):
    VCC_INT.DAC.set_voltage(0, i)
    time.sleep(0.1)
    get = VCC_INT.ADC.get_voltage(0)*2
    print('Set: ' + str(i) + ' Get: ' + str(get))



