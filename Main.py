from PowerSourceControl import PowerSource
from SerialCommunications import SerialCommunicator

RS485 = SerialCommunicator()

#RS485.chain_scan()

VCC_INT = PowerSource(address=0xA, communicator=RS485)

VCC_INT.get_zero_error()
VCC_INT.set_current(1)
VCC_INT.set_voltage(5.5)
VCC_INT.write_status_to_db()


