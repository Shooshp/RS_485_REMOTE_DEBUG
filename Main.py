from AVR import Atmega16RegisterMap as AVR
from PowerSourceControl import PowerSource
from SerialCommunications import SerialCommunicator
from DataBase.DataBaseConnector import DataBaseCommunicator
from HostController import DevicePrefixes as device_list

DB_CONNECTOR = DataBaseCommunicator()

RS485 = SerialCommunicator()

#RS485.chain_scan(device_list)

VCC_INT = PowerSource(address=0xA, communicator=RS485, db_connector=DB_CONNECTOR)
VCC_INT.calibration()


#VCC_INT.clear_device_id()