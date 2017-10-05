from SerialCommunications import Communicator
from HostController import  HostController
from PowerSourceControl import PowerSource

Communicator.open_port()


VCC_INT = PowerSource(address=0xAA)
VCC_LOAD = PowerSource(address=0xA3)

print(VCC_LOAD.INSTANCE_NAME)

VCC_INT.set_voltage(1500)
VCC_LOAD.set_current(3200)