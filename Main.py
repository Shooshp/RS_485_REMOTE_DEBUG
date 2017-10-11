from AVR import Atmega16RegisterMap as AVR
from PowerSourceControl import PowerSource
from SerialCommunications import Communicator
from mysql.connector import MySQLConnection, Error
from DataBase.DataBaseConfiguration import read_db_config

db_config = read_db_config()
conn = MySQLConnection(**db_config)
if conn.is_connected():
    print('Successfully connected to local DB')

RS485 = Communicator()

RS485.chain_scan()

VCC_INT = PowerSource(address=0xAA, communicator= RS485)


#VCC_INT.clear_device_id()