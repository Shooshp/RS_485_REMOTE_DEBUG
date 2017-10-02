import serial
import time
import RPi.GPIO as GPIO
import struct
from PyCRC.CRC16 import CRC16


class Communicator(object):

    def __init__(self,
                 port='/dev/ttyS0',
                 baudrate=9600,
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

        self.BUFFER_ARRAY = bytearray()

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.EN_485_PIN, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.EN_TX_PIN, GPIO.OUT, initial=GPIO.HIGH)

        self.rs485_port = serial.Serial(
            port=self.PORT,
            baudrate=self.BAUDRATE,
            parity=self.PARITY,
            stopbits=self.STOPBITS,
            bytesize=self.BYTESIZE,
            timeout=self.TIMEOUT
        )

        self.usleep = lambda x: time.sleep(x/1000000.0)

    def write_to_serial(self, command, data, address):
        self.rs485_port.write(self.enclose(command, data, address))
        self.wait_for_an_answer()

    def read_from_serial(self):
        self.rs485_port.read()

    def enclose(self, command, data, address):

        data_lenght = len(data)

        self.BUFFER_ARRAY = struct.pack('BBB',address,command,data_lenght) + data
        CRC = CRC16().calculate(self.BUFFER_ARRAY)
        self.BUFFER_ARRAY = self.BUFFER_ARRAY + struct.pack('>H', CRC)

        print('Full Message: ' + str(self.BUFFER_ARRAY))
        return self.BUFFER_ARRAY

    def chain_scan(self):
        for address in range(255):
            self.write_to_serial('Whois'.encode(), address)

    def wait_for_an_answer(self):
        self.usleep(40000)
        GPIO.output(self.EN_TX_PIN, 0)

        self.BUFFER_ARRAY = self.rs485_port.read(3)

        GPIO.output(self.EN_TX_PIN, 1)

        print('Got Replay: ' + str(self.BUFFER_ARRAY))
        return self.BUFFER_ARRAY

