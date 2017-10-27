import numpy as np
from DataBase.ORMDataBase import device_types, db, power_source_calibration as calib
from PowerSourceControl import PowerSource
from SerialCommunications import SerialCommunicator
from DataBase.DataBaseConnector import DataBaseCommunicator
from HostController import DevicePrefixes as device_list

DB_CONNECTOR = DataBaseCommunicator()

RS485 = SerialCommunicator()

#RS485.chain_scan(device_list)

array = np.arange(0, 4, 0.1)

VCC_INT = PowerSource(address=0xA, communicator=RS485, db_connector=DB_CONNECTOR)

db.connect()

print(hex(device_types.get(TYPE = 'PowerSource').ADDRESS_PREFIX))

for type in device_types.select():
    print(type.TYPE)

for value in calib.select().where((calib.V_GET > '0.2')&(calib.V_GET < '0.21')):
    print(value.V_SET)