from PowerSourceControl import PowerSource
from SerialCommunications import SerialCommunicator
import HostnameSetup

RS485 = SerialCommunicator()

#  RS485.chain_scan()

#  VCC_INT = PowerSource(address=0xA, communicator=RS485)

HostnameSetup.SetHostname('Azazaz')