import serial
import time
import RPi.GPIO as GPIO
import struct
from PyCRC.CRC16 import CRC16
from DataBase.ORMDataBase import device_index

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

    def write_to_serial(self, host):

        self.HOST = host

        status = 0
        error_counter = 0

        while not status and error_counter < 100:
            self.BUFFER_ARRAY = struct.pack('BBB', self.HOST.ADDRESS, self.HOST.COMMAND, len(self.HOST.ARRAY_TO_SEND)) \
                           + self.HOST.ARRAY_TO_SEND
            self.CURRENT_CRC = CRC16().calculate(self.BUFFER_ARRAY)
            self.BUFFER_ARRAY = self.BUFFER_ARRAY + struct.pack('>H', self.CURRENT_CRC)

            self.RS_485.write(self.BUFFER_ARRAY)
            self.delay_calculate()

            callback = self.wait_for_an_answer()

            if callback:
                if struct.unpack('B', callback[0:1])[0] == self.HOST.ADDRESS and\
                                struct.unpack('>H', callback[1:3])[0] == self.CURRENT_CRC:
                    status = 1
                else:
                    error_counter += 1
            else:
                error_counter += 1

        if status:
            if error_counter:
                error_message = ' During transmission occurred ' + str(error_counter + 1) + ' errors!'
            else:
                error_message = ' Without errors.'

            #print('Data was successfully send to host '
            #      + str(self.HOST.OBJECT_TYPE) + ': '
            #      + str(self.HOST.INSTANCE_NAME) + ' at address '
            #      + str(hex(self.HOST.ADDRESS)) + '!'
            #      + error_message)

        else:
            print('Failed to reach host '
                  + str(self.HOST.OBJECT_TYPE) + ': '
                  + str(self.HOST.INSTANCE_NAME) + ' at address '
                  + str(hex(self.HOST.ADDRESS)) + '!')

    def read_from_serial(self, host):
        self.HOST = host
        status = 0
        error_counter = 0

        while not status and error_counter < 100:
            self.write_to_serial(self.HOST)
            callback = self.wait_for_an_reply()

            if callback:
                if struct.unpack('B', callback[0:1])[0] == self.HOST.ADDRESS and\
                                struct.unpack('>H', callback[2:4])[0] == self.CURRENT_CRC:
                    status = 1
                    self.HOST.ARRAY_TO_RECEIVE = struct.unpack('B', callback[1:2])[0]
                else:
                    error_counter += 1
            else:
                error_counter += 1

        if status:
            if error_counter:
                error_message = ' During transmission occurred ' + str(error_counter + 1) + ' errors!'
            else:
                error_message = ' Without errors.'

         #   print('Data was successfully read from host '
         #         + str(self.HOST.OBJECT_TYPE) + ': '
         #         + str(self.HOST.INSTANCE_NAME) + ' at address '
         #         + str(hex(self.HOST.ADDRESS)) + '!'
         #         + error_message)

        else:
            print('Failed to get reply from host '
                  + str(self.HOST.OBJECT_TYPE) + ': '
                  + str(self.HOST.INSTANCE_NAME) + ' at address '
                  + str(hex(self.HOST.ADDRESS)) + '!')

    def chain_scan(self, trys=5):
        hosts = []

        for device in device_index.select():
            for address_bit in range(0,15):
                address = device.address_prefix | address_bit
                ARRAY_TO_SEND = struct.pack('>H', 0x0)
                command = 0x0
                status = 0
                error_counter = 0
                self.BUFFER_ARRAY = struct.pack('BBB', address, command, len(ARRAY_TO_SEND)) + ARRAY_TO_SEND
                self.CURRENT_CRC = CRC16().calculate(self.BUFFER_ARRAY)
                self.BUFFER_ARRAY = self.BUFFER_ARRAY + struct.pack('>H', self.CURRENT_CRC)

                while not status and error_counter < trys:
                    self.RS_485.write(self.BUFFER_ARRAY)
                    self.delay_calculate()
                    callback = self.wait_for_an_answer()

                    if callback:
                        if struct.unpack('B', callback[0:1])[0] == address and \
                                        struct.unpack('>H', callback[1:3])[0] == self.CURRENT_CRC:
                            status = 1
                        else:
                            error_counter += 1
                    else:
                        error_counter += 1

                if status:
                    hosts.append([device.device_type, hex(address)])
        print(hosts)
        print(str(len(hosts)) + ' host was found!')
        return hosts

    def wait_for_an_answer(self):
        GPIO.output(self.EN_TX_PIN, 0)
        replay_buffer = self.RS_485.read(size=3)
        GPIO.output(self.EN_TX_PIN, 1)
        self.usleep(800)
        return replay_buffer

    def wait_for_an_reply(self):
        GPIO.output(self.EN_TX_PIN, 0)
        replay_buffer = self.RS_485.read(size=4)
        GPIO.output(self.EN_TX_PIN, 1)
        self.usleep(800)
        return replay_buffer

    def delay_calculate(self):
        time.sleep(((self.BYTESIZE + self.STOPBITS + 1) / self.BAUDRATE) * len(self.BUFFER_ARRAY))

    def msleep(self, ms):
        time.sleep(ms / 1000.0)

    def usleep(self, us):
        time.sleep(us / 1000000.0)
