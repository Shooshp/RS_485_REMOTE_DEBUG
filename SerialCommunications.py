import serial
import RPi.GPIO as GPIO
from PyCRC.CRC16 import CRC16
from struct import pack


class Communicator(object):

    def __init__(self,
                 port='/dev/ttyS0',
                 baudrate=9600,
                 parity=serial.PARITY_NONE,
                 stopbits=serial.STOPBITS_ONE,
                 bytesize=serial.EIGHTBITS,
                 timeout=1,
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

        self.BIN = bytearray()

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

    def write_to_serial(self, data, address):
        self.rs485_port.write(self.enclose(data, address))

    def enclose(self, data, address):
        is_string = isinstance(data, str)
        is_bytes = isinstance(data, bytes)

        if not is_string and not is_bytes:
            raise Exception("Please provide a string or a byte sequence as argument for calculation.")

        CRC16().crc16_constant = self.CRC_CONSTANT

        self.BIN = 'Address: '.encode() + pack('B', address) + '\n\r'.encode()
        self.BIN = self.BIN + 'Command: '.encode() + data + '\n\r'.encode()
        self.BIN = self.BIN + 'CRC: '.encode() + pack('H', CRC16().calculate(self.BIN)) + '\n\r'.encode()

        print(self.BIN)

        return self.BIN
