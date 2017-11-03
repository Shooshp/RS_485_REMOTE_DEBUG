import threading, asyncore, time
from PowerSourceControl import PowerSource
from SerialCommunications import SerialCommunicator
from EthernetCommunications import ListenerServer

# RS485 = SerialCommunicator()
# RS485.chain_scan()
# VCC_INT = PowerSource(address=0xA, communicator=RS485)

def main_process():
    while True:
        print('Auxilary Loop')
        time.sleep(1)


if  __name__ == "__main__":
    server = ListenerServer()

    proc1 = threading.Thread(target=main_process)
    proc1.daemon = True
    proc1.start()

    while 1:
        print('Main Loop')
        time.sleep(1)