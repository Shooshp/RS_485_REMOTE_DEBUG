import SerialCommunications
from PowerSourceControl import PowerSource

RS485 = SerialCommunications.Communicator(timeout=100)


VCC_INT = PowerSource(RS485, address=0x66)
VCC_LOAD = PowerSource(RS485, address=0xA3)

counter = 0

RS485.chain_scan()

while 1:
    VCC_INT.set_voltage(counter)
    VCC_LOAD.set_current(counter)
    counter += 1
