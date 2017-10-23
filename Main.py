from AVR import Atmega16RegisterMap as AVR
import numpy as np
from PowerSourceControl import PowerSource
from SerialCommunications import SerialCommunicator
from DataBase.DataBaseConnector import DataBaseCommunicator
from HostController import DevicePrefixes as device_list

DB_CONNECTOR = DataBaseCommunicator()

RS485 = SerialCommunicator()

#RS485.chain_scan(device_list)


VCC_INT = PowerSource(address=0xA, communicator=RS485, db_connector=DB_CONNECTOR)

array = np.arange(0.0,4.0,0.1)

for i in array:
    VCC_INT.DAC.set_voltage(0,i)
    print(VCC_INT.measure(chanel=0,division_coefficient=2))

#VCC_INT.clear_device_id()