import SerialCommunications
from PowerSourceControl import PowerSource

RS485 = SerialCommunications.Communicator()

VCC_INT = PowerSource(RS485, address=0xAA)
VCC_LOAD = PowerSource(RS485, address=0xA3)

VCC_INT.set_voltage(1000)
VCC_LOAD.set_current(4200)

