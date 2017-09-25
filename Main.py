import SerialCommunications
from PowerSourceControl import PowerSource

RS485 = SerialCommunications.Communicator(timeout=100)
VCC_INT = PowerSource(RS485, address=0x66)

counter = 0

while 1:
    VCC_INT.set_voltage(counter)
    counter += 1
