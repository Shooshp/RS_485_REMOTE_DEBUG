import threading, time
from ORMDataBase import power_source_settings
from PowerSourceControl import PowerSource
from SerialCommunications import SerialCommunicator
from EthernetCommunications import ListenerServer, EventManager

# VCC_INT = PowerSource(address=0xA, communicator=RS485)

def initialization():
    power_source_settings.truncate_table()  # Clear Settings Table
    RS485 = SerialCommunicator() # Initialize RS-485 communicator
    host_list = RS485.chain_scan()  # Get all connected hosts with their respective types
    current_power_source_list = []
    for host in host_list:
        if  host[0] == 'PowerSource':
            current_power_source_list.append(PowerSource((host[1]&0xF), RS485))

    print(host_list)

def main_process():
    while True:
        if  EventManager.data:
            time.sleep(1)
            print("Get data ", EventManager.data)
            EventManager.data=0


if  __name__ == "__main__":
    initialization()

    server = ListenerServer()
    proc1 = threading.Thread(target=main_process)
    proc1.daemon = True
    proc1.start()

    while 1:
        print('Main Loop')
        time.sleep(1)