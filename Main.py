from AVR import Atmega16RegisterMap as AVR
import numpy as np
from PowerSourceControl import PowerSource
from SerialCommunications import SerialCommunicator
from DataBase.DataBaseConnector import DataBaseCommunicator
from HostController import DevicePrefixes as device_list

DB_CONNECTOR = DataBaseCommunicator()

RS485 = SerialCommunicator()

#RS485.chain_scan(device_list)

array = np.arange(0, 4, 0.1)

VCC_INT = PowerSource(address=0xA, communicator=RS485, db_connector=DB_CONNECTOR)

VCC_INT.set_current(current=1)
VCC_INT.set_voltage(voltage=5.5)

for i in range(0, 20):
    VCC_INT.write_status_to_db()