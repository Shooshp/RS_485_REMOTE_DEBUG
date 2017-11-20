import threading, time
from ORMDataBase import power_source_settings, power_source_current_tasks
from PowerSourceControl import PowerSource
from SerialCommunications import SerialCommunicator
from EthernetCommunications import ListenerServer, EventManager, UDPBroadcaster

# VCC_INT = PowerSource(address=0xA, communicator=RS485)

current_power_source_list = []

def initialization():
    power_source_current_tasks.truncate_table() # Clear Task Table
    power_source_settings.truncate_table()  # Clear Settings Table
    RS485 = SerialCommunicator() # Initialize RS-485 communicator
    host_list = RS485.chain_scan()  # Get all connected hosts with their respective types

    for host in host_list:
        if  host[0] == 'PowerSource':
            current_power_source_list.append(PowerSource((host[1]&0xF), RS485))

    print(host_list)

def main_process():
    while True:
        if  EventManager.CurrentTaskId is not 0:
            Task = power_source_current_tasks.select().where(power_source_current_task_id = EventManager.CurrentTaskId)

            if Task.power_source_current_task_name == "SetVoltage":
                for power_source in current_power_source_list:
                    if power_source.DEVICE_ID.hex() == Task.power_source_current_task_device_uuid:
                        EventManager.PowerSourceStatus = "Setting Voltage to chanel: " + str(power_source.ADDRESS.hex())
                        power_source.update_settings()
                        power_source.set_voltage(power_source.VOLTAGE)
                        EventManager.TaskCompleted(EventManager.CurrentTaskId)

            if Task.power_source_current_task_name == "SetCurrent":
                for power_source in current_power_source_list:
                    if power_source.DEVICE_ID.hex() == Task.power_source_current_task_device_uuid:
                        EventManager.PowerSourceStatus = "Setting Current to chanel: " + str(power_source.ADDRESS.hex())
                        power_source.update_settings()
                        power_source.set_current(power_source.CURRENT)
                        EventManager.TaskCompleted(EventManager.CurrentTaskId)

            if Task.power_source_current_task_name == "Calibrate":
                for power_source in current_power_source_list:
                    if power_source.DEVICE_ID.hex() == Task.power_source_current_task_device_uuid:
                        EventManager.PowerSourceStatus = "Calibrating chanel: " + str(power_source.ADDRESS.hex())
                        power_source.DAC.clear()
                        power_source.turn_off()
                        power_source.calibration()
                        EventManager.TaskCompleted(EventManager.CurrentTaskId)

            if Task.power_source_current_task_name == "ShutDown":
                for power_source in current_power_source_list:
                    if power_source.DEVICE_ID.hex() == Task.power_source_current_task_device_uuid:
                        EventManager.PowerSourceStatus = "Shutting Down chanel: " + str(power_source.ADDRESS.hex())
                        power_source.turn_off()
                        EventManager.TaskCompleted(EventManager.CurrentTaskId)


        for power_source in current_power_source_list:
            if power_source.IS_ON:
                power_source.write_status_to_db()



if  __name__ == "__main__":
    initialization()

    StatusServer = ListenerServer(port= 10236)
    ConnectionChecker =  UDPBroadcaster(10237)
    proc1 = threading.Thread(target=main_process)
    proc1.daemon = True
    proc1.start()

    while 1:
        print('Main Loop')
        time.sleep(1)