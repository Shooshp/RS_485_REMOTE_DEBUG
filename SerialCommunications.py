import serial
import time
import RPi.GPIO as GPIO
from PyCRC.CRC16 import CRC16

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

    def WriteToSerial(self, data, address):
        self.rs485_port.write(self.Enclose(data, address))

    def ReadFromSerial(self):
        self.rs485_port.read()

    def Enclose(self, data, address):
        is_string = isinstance(data, str)
        is_bytes = isinstance(data, bytes)

        if not is_string and not is_bytes:
            raise Exception("Please provide a string or a byte sequence as argument for calculation.")

        CRC16().crc16_constant = self.CRC_CONSTANT

        self.BUFFER_ARRAY = 'Address: '.encode() + hex(address).encode()
        self.BUFFER_ARRAY = self.BUFFER_ARRAY + ' Command: '.encode() + data
        self.BUFFER_ARRAY = self.BUFFER_ARRAY + ' CRC: '.encode() + hex(CRC16().calculate(self.BUFFER_ARRAY)).encode() + '\r\n'.encode()

        print(self.BUFFER_ARRAY)

        return self.BUFFER_ARRAY

    def ChainScan(self):
        for address in range(255):
            self.WriteToSerial('Whois'.encode(), address)

    def WaitForAnAnswer(self):
        GPIO.output(self.EN_TX_PIN,0)

        for counter in range (100):
            self.BUFFER_ARRAY = self.rs485_port.readline()


            if not self.BUFFER_ARRAY:
                self.usleep(10)

        GPIO.output(self.EN_TX_PIN,1)

        return self.BUFFER_ARRAY







