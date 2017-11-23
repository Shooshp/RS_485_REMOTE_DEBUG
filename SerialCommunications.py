import struct
import time
import serial
import uuid
from ORMDataBase import DeviceList, Devices
import PyCRC.CRC16
import RPi.GPIO as GPIO


class SerialCommunicator(object):

    def __init__(self,
                 port='/dev/ttyS0',
                 baudrate=1000000,
                 parity=serial.PARITY_NONE,
                 stopbits=serial.STOPBITS_ONE,
                 bytesize=serial.EIGHTBITS,
                 timeout=0.005,
                 en_485_pin=12,
                 en_tx_pin=16,
                 crc_constant=0xA001
                 ):

        self.PORT = port
        self.BAUDRATE = baudrate
        self.PARITY = parity
        self.STOPBITS = stopbits
        self.BYTESIZE = bytesize
        self.TIMEOUT = timeout
        self.EN_485_PIN = en_485_pin
        self.EN_TX_PIN = en_tx_pin
        self.CRC_CONSTANT = crc_constant

        self.HOST = None
        self.CURRENT_CRC = None
        self.BUFFER_ARRAY = None

        self.RS_485 = serial.Serial(
            port=self.PORT,
            baudrate=self.BAUDRATE,
            parity=self.PARITY,
            stopbits=self.STOPBITS,
            bytesize=self.BYTESIZE,
            timeout=self.TIMEOUT
        )

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.EN_485_PIN, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.EN_TX_PIN, GPIO.OUT, initial=GPIO.HIGH)
        self.msleep(5)

    def write_to_serial(self, address, command, data):
        status = 0
        error_counter = 0

        while not status and error_counter < 100:
            self.pack_data(address, command, data)
            self.RS_485.write(self.BUFFER_ARRAY)
            self.delay_calculate()

            callback = self.wait_for_an_answer(size=3)

            if callback:
                if self.check_callback_crc(callback, address):
                    status = 1
                else:
                    error_counter += 1
            else:
                error_counter += 1

        if status:
            if error_counter:
                error_message = ' During transmission occurred ' + str(error_counter + 1) + ' errors!'
                print('Data was successfully send to host  at address ' + str(hex(address)) + '!' + error_message)
        else:
            print('Failed to reach host at address ' + str(hex(address)) + '!')

    def read_from_serial(self, address, command, data):
        status = 0
        error_counter = 0
        data_receive = bytearray()

        while not status and error_counter < 100:
            self.write_to_serial(address, command, data)
            callback = self.wait_for_an_answer(size=4)

            if callback:
                if self.check_callback_crc(callback, address):
                    status = 1
                    data_receive = struct.unpack('B', callback[1:2])[0]
                else:
                    error_counter += 1
            else:
                error_counter += 1

        if status:
            if error_counter:
                error_message = ' During transmission occurred ' + str(error_counter + 1) + ' errors!'
                print('Data was successfully read from host  at address ' + str(hex(address)) + '!' + error_message)
        else:
            print('Failed to get reply from host at address ' + str(hex(address)) + '!')
        return data_receive

    def chain_scan(self, attempts=5):
        hosts = []
        print('Scanning device chain...')
        for Device in DeviceList.select():
            for address_bit in range(0, 16):
                Address = Device.AddressPrefix | address_bit
                print('Looking for ', Device.Type, ' with address ', hex(Address))
                command = 0x0
                data = struct.pack('>H', 0x0)
                host_uuid = None
                status = 0
                error_counter = 0
                self.pack_data(Address, command, data)

                while not status and error_counter < attempts:
                    self.RS_485.write(self.BUFFER_ARRAY)
                    self.delay_calculate()
                    callback = self.wait_for_an_answer(size=3)

                    if callback:
                        if self.check_callback_crc(callback, Address):
                            status = 1
                            host_uuid = self.device_uuid_get(Address)
                            if not host_uuid:
                                self.device_uuid_set(Address)
                                host_uuid = self.device_uuid_get(Address)
                        else:
                            error_counter += 1
                    else:
                        error_counter += 1

                if status:
                    print('>>> Get reply from ', Device.Type, ' with address ', hex(Address))
                    Devices.get_or_create(
                        UUID=host_uuid.hex(),
                        Type=Device.Type,
                        Address=Address
                    )
                    hosts.append([Device.Type, Address, host_uuid.hex()])

        print(str(len(hosts)) + ' host was found!')
        return hosts

    def wait_for_an_answer(self, size):
        GPIO.output(self.EN_TX_PIN, 0)
        replay_buffer = self.RS_485.read(size=size)
        GPIO.output(self.EN_TX_PIN, 1)
        self.usleep(800)
        return replay_buffer

    def delay_calculate(self):
        time.sleep(((self.BYTESIZE + self.STOPBITS + 1) / self.BAUDRATE) * len(self.BUFFER_ARRAY))

    @staticmethod
    def msleep(ms):
        time.sleep(ms / 1000.0)

    @staticmethod
    def usleep(us):
        time.sleep(us / 1000000.0)

    def pack_data(self, address, command, data):
        self.BUFFER_ARRAY = struct.pack('BBB', address, command, len(data)) + data
        self.CURRENT_CRC = PyCRC.CRC16.CRC16().calculate(self.BUFFER_ARRAY)
        self.BUFFER_ARRAY = self.BUFFER_ARRAY + struct.pack('>H', self.CURRENT_CRC)

    def check_callback_crc(self, callback, address):
        if (struct.unpack('B', callback[0:1])[0] == address) \
                and (struct.unpack('>H', callback[(len(callback)-2):len(callback)])[0] == self.CURRENT_CRC):
            return True
        else:
            return False

    def device_uuid_get(self, address):
        get_id_command = 5
        device_uuid = bytearray()
        status = 0
        for device_id_byte in range(0, 16):
            data = struct.pack('>H', device_id_byte)
            receive_data = self.read_from_serial(address, get_id_command, data)
            device_uuid.append(receive_data)
            if receive_data == 0xFF:
                status += 1

        if status != 16:
            return device_uuid
        else:
            return 0

    def device_uuid_set(self, address):
        set_id_command = 6
        unique_id = uuid.uuid4()
        for device_id_byte in range(0, 16):
            data = struct.pack('>HB', device_id_byte, unique_id.bytes[device_id_byte])
            self.write_to_serial(address, set_id_command, data)
            time.sleep(0.01)

    def device_uuid_clear(self, address):
        set_id_command = 6
        for device_id_byte in range(0, 16):
            data = struct.pack('>HB', device_id_byte, 0xFF)
            self.write_to_serial(address, set_id_command, data)
