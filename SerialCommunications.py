import serial
import time
import RPi.GPIO as GPIO
import struct
from PyCRC.CRC16 import CRC16

class Communicator(object):

    def __init__(self,
                 port='/dev/ttyS0',
                 baudrate=1000000,
                 parity=serial.PARITY_NONE,
                 stopbits=serial.STOPBITS_ONE,
                 bytesize=serial.EIGHTBITS,
                 timeout=0.1,
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

        self.CURRENT_CRC = int()

        self.BUFFER_ARRAY = bytearray()

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.EN_485_PIN, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.EN_TX_PIN, GPIO.OUT, initial=GPIO.HIGH)

        self.rs485_port = serial.Serial(
            port=self.PORT,
            baudrate=self.BAUDRATE,
            parity=self.PARITY,
            stopbits=self.STOPBITS,
            bytesize=self.BYTESIZE,
            timeout=self.TIMEOUT,
        )

        self.usleep = lambda x: time.sleep(x / 1000000.0)
        self.msleep = lambda x: time.sleep(x / 1000.0)

        self.msleep(5)

    def write_to_serial(self, command, data, address, instance_name, object_type):
        status = 0
        error_counter = 0

        while not status and error_counter < 100:
            self.rs485_port.write(self.enclose(command, data, address))
            # print('Full Message: ' + str(self.BUFFER_ARRAY))
            self.delay_calculate(len(self.enclose(command,data,address)))

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
            if error_counter:
                error_message = ' During transmission occurred ' + str(error_counter+1) + ' errors!'
            else:
                error_message =' Without errors.'

            print('Data was successfully send to host ' + str(object_type) + ': ' + str(instance_name) + ' at address '
                  + str(hex(address)) + '!' + error_message)

        else:
            print('Failed to reach host '  + str(object_type) + ': ' + str(instance_name) + ' at address '
                  + str(hex(address)) + '!')

    def read_from_serial(self):
        self.rs485_port.read()

    def enclose(self, command, data, address):
        data_length = len(data)

        self.BUFFER_ARRAY = struct.pack('BBB', address, command, data_length) + data
        self.CURRENT_CRC = CRC16().calculate(self.BUFFER_ARRAY)
        self.BUFFER_ARRAY = self.BUFFER_ARRAY + struct.pack('>H', self.CURRENT_CRC)
        return self.BUFFER_ARRAY

    def chain_scan(self):
        for address in range(255):
            self.write_to_serial(command=0x0,  data='Whois'.encode(), address=address)

    def wait_for_an_answer(self):
        GPIO.output(self.EN_TX_PIN, 0)
        replay_buffer = self.rs485_port.read(size=3)
        GPIO.output(self.EN_TX_PIN, 1)
        #print('Got Replay: ' + str(replay_buffer))
        return replay_buffer

    def delay_calculate(self, size_of_transmission):
        time_to_sleep = ((self.BYTESIZE + self.STOPBITS + 1) / self.BAUDRATE) * size_of_transmission
        time.sleep(time_to_sleep)

