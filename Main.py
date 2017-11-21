import threading
import time
from ORMDataBase import power_source_settings, power_source_current_tasks
from PowerSourceControl import PowerSource
from SerialCommunications import SerialCommunicator
from EthernetCommunications import ListenerServer, EventManager, UDPBroadcaster

# VCC_INT = PowerSource(address=0xA, communicator=RS485)

current_power_source_list = []


def initialization():
    power_source_current_tasks.truncate_table()  # Clear Task Table
    power_source_settings.truncate_table()  # Clear Settings Table
    r_s485 = SerialCommunicator()  # Initialize RS-485 communicator
    host_list = r_s485.chain_scan()  # Get all connected hosts with their respective types

    for host in host_list:
        if host[0] == 'PowerSource':
            current_power_source_list.append(PowerSource((host[1] & 0xF), r_s485))

    print(host_list)


def main_process():
    while True:
        if EventManager.CurrentTaskId is not 0:
            task = power_source_current_tasks.get(power_source_current_tasks.power_source_current_task_id==EventManager.CurrentTaskId)
            task_name = task.power_source_current_task_name.power_source_task_name
            target_device_uuid = task.power_source_current_task_device_uuid.devices_on_tester_uuid
            print(task_name)
            print(target_device_uuid.encode('utf-8').hex())
            for power_source in current_power_source_list:
                print(str(power_source.DEVICE_ID))

            if task_name == "SetVoltage":
                for power_source in current_power_source_list:
                    if power_source.DEVICE_ID.hex() == task.power_source_current_task_device_uuid:
                        EventManager.PowerSourceStatus = "Setting Voltage to chanel: " + str(power_source.ADDRESS.hex())
                        power_source.set_voltage(task.power_source_current_task_argument)
                        EventManager.TaskCompleted(EventManager.CurrentTaskId)

            if task_name == "SetCurrent":
                print(str(task.power_source_current_task_device_uuid.devices_on_tester_uuid.hex()))
                for power_source in current_power_source_list:
                    if power_source.DEVICE_ID.hex() == task.power_source_current_task_device_uuid:
                        EventManager.PowerSourceStatus = "Setting Current to chanel: " + str(power_source.ADDRESS.hex())
                        power_source.set_current(task.power_source_current_task_argument)
                        EventManager.TaskCompleted(EventManager.CurrentTaskId)

            if task_name == "Calibrate":
                for power_source in current_power_source_list:
                    if power_source.DEVICE_ID.hex() == task.power_source_current_task_device_uuid:
                        EventManager.PowerSourceStatus = "Calibrating chanel: " + str(power_source.ADDRESS.hex())
                        power_source.DAC.clear()
                        power_source.turn_off()
                        power_source.calibration()
                        EventManager.TaskCompleted(EventManager.CurrentTaskId)

            if task_name == "ShutDown":
                for power_source in current_power_source_list:
                    if power_source.DEVICE_ID.hex() == task.power_source_current_task_device_uuid:
                        EventManager.PowerSourceStatus = "Shutting Down chanel: " + str(power_source.ADDRESS.hex())
                        power_source.turn_off()
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
