import serial
import RPi.GPIO as GPIO
from Chek_sum_and_addr import data_packet


class Rs485Communication(object):

    def __init__(self,
                 port = '/dev/ttyS0',
                 baudrate = 9600,
                 parity = serial.PARITY_NONE,
                 stopbits = serial.STOPBITS_ONE,
                 bytesize = serial.EIGHTBITS,
                 timeout = 1,
                 en_485_pin = 12,
                 en_tx_pin = 16,
                 addr = 0x0,):

        self.PORT = port
        self.BAUDRATE = baudrate
        self.PARITY = parity
        self.STOPBITS = stopbits
        self.BYTESIZE = bytesize
        self.TIMEOUT = timeout
        self.EN_485_PIN = en_485_pin
        self.EN_TX_PIN = en_tx_pin
        self.ADDRESS = addr

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.EN_485_PIN, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.EN_TX_PIN, GPIO.OUT, initial=GPIO.HIGH)

        self.packet = data_packet(addr=self.ADDRESS)

        self.rs485_port = serial.Serial(
            port=self.PORT,
            baudrate=self.BAUDRATE,
            parity=self.PARITY,
            stopbits=self.STOPBITS,
            bytesize=self.BYTESIZE,
            timeout=self.TIMEOUT
        )

    def write_and_read(self, data):
        self.rs485_port.write(self.packet.pack_data(data))