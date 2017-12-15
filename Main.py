import threading
import time
from ORMDataBase import Settings, CurrentTasks, Calibration
from PowerSourceControl import PowerSource
from SerialCommunications import SerialCommunicator
from EthernetCommunications import ListenerServer, EventManager, UDPBroadcaster

# VCC_INT = PowerSource(address=0xA, communicator=RS485)

current_power_source_list = []


def initialization():
    CurrentTasks.truncate_table()  # Clear Task Table
    Settings.truncate_table()  # Clear Settings Table
    r_s485 = SerialCommunicator()  # Initialize RS-485 communicator
    host_list = r_s485.chain_scan()  # Get all connected hosts with their respective types

    for host in host_list:
        if host[0] == 'PowerSource':
            current_power_source_list.append(PowerSource((host[1] & 0xF), r_s485))

    for powersource in current_power_source_list:
        if powersource.isCalibrated is not True:
            print('Calibrating :' + str(powersource.ADDRESS))
            powersource.calibration()

    print(host_list)

def main_process():
    while True:
        if EventManager.CurrentTaskId is not 0:
            Task = CurrentTasks.get(CurrentTasks.id == EventManager.CurrentTaskId, CurrentTasks.IsCompleted == False)
            TaskName = Task.Name.Name
            TaskUUID = Task.UUID.UUID

            if TaskName == "SetVoltage":
                for power_source in current_power_source_list:
                    if power_source.DEVICE_ID.hex() == TaskUUID:
                        EventManager.PowerSourceStatus = "Setting Voltage to chanel: " + str(hex(power_source.ADDRESS))
                        print(EventManager.PowerSourceStatus, 'Value: ', str(Task.Value))
                        power_source.set_voltage(float(Task.Value))
                        EventManager.TaskCompleted(EventManager.CurrentTaskId)

            if TaskName == "SetCurrent":
                for power_source in current_power_source_list:
                    if power_source.DEVICE_ID.hex() == TaskUUID:
                        EventManager.PowerSourceStatus = "Setting Current to chanel: " + str(hex(power_source.ADDRESS))
                        print(EventManager.PowerSourceStatus, 'Value: ', str(Task.Value))
                        power_source.set_current(float(Task.Value))
                        EventManager.TaskCompleted(EventManager.CurrentTaskId)

            if TaskName == "Calibrate":
                for power_source in current_power_source_list:
                    if power_source.DEVICE_ID.hex() == TaskUUID:
                        EventManager.PowerSourceStatus = "Calibrating chanel: " + str(hex(power_source.ADDRESS))
                        print(EventManager.PowerSourceStatus)
                        power_source.DAC.clear()
                        power_source.turn_off()
                        power_source.calibration()
                        EventManager.TaskCompleted(EventManager.CurrentTaskId)

            if TaskName == "ShutDown":
                for power_source in current_power_source_list:
                    if power_source.DEVICE_ID.hex() == TaskUUID:
                        EventManager.PowerSourceStatus = "Shutting Down chanel: " + str(hex(power_source.ADDRESS))
                        print(EventManager.PowerSourceStatus)
                        power_source.turn_off()
                        EventManager.TaskCompleted(EventManager.CurrentTaskId)

            if TaskName == "TurnOn":
                for power_source in current_power_source_list:
                    if power_source.DEVICE_ID.hex() == TaskUUID:
                        EventManager.PowerSourceStatus = "Turning on chanel: " + str(hex(power_source.ADDRESS))
                        print(EventManager.PowerSourceStatus)
                        power_source.turn_on()
                        EventManager.TaskCompleted(EventManager.CurrentTaskId)

        for power_source in current_power_source_list:
            if power_source.IS_ON:
                power_source.write_status_to_db()


if __name__ == "__main__":
    initialization()

    StatusServer = ListenerServer(port=10236)
    ConnectionChecker = UDPBroadcaster(10237)
    main_thread = threading.Thread(target=main_process)
    main_thread.daemon = True
    main_thread.start()

    while 1:
        print('Main Loop')
        time.sleep(1)

