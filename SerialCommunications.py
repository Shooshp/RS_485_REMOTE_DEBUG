import serial
import time
import RPi.GPIO as GPIO
import struct
from PyCRC.CRC16 import CRC16


class Communicator(object):
    port = '/dev/ttyS0'
    baudrate = 1000000
    parity = serial.PARITY_NONE
    stopbits = serial.STOPBITS_ONE
    bytesize = serial.EIGHTBITS
    timeout = 0.01
    en_485_pin = 12
    en_tx_pin = 16
    crc_constant = 0xA001
    CURRENT_CRC = int()

    HOST = None

    rs485_port = serial.Serial(
        port=port,
        baudrate=baudrate,
        parity=parity,
        stopbits=stopbits,
        bytesize=bytesize,
        timeout=timeout
    )

    @staticmethod
    def open_port():

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(Communicator.en_485_pin, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(Communicator.en_tx_pin,  GPIO.OUT, initial=GPIO.HIGH)

        msleep(5)

    @staticmethod
    def write_to_serial(address, command, data, name, type):

        status = 0
        error_counter = 0

        while not status and error_counter < 100:
            BUFFER_ARRAY = struct.pack('BBB', address, command, len(data)) + data
            CURRENT_CRC = CRC16().calculate(BUFFER_ARRAY)
            BUFFER_ARRAY = BUFFER_ARRAY + struct.pack('>H', CURRENT_CRC)


            Communicator.rs485_port.write(BUFFER_ARRAY)
            Communicator.delay_calculate(BUFFER_ARRAY)

            callback = Communicator.wait_for_an_answer()

            if callback:
                if struct.unpack('B', callback[0:1])[0] == address and struct.unpack('>H', callback[1:3])[0] == CURRENT_CRC:
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

            print('Data was successfully send to host '
                  + str(type) + ': '
                  + str(name) + ' at address '
                  + str(hex(address)) + '!'
                  + error_message)

        else:
            print('Failed to reach host '
                  + str(type) + ': '
                  + str(name) + ' at address '
                  + str(hex(address)) + '!')

    @staticmethod
    def read_from_serial():
        Communicator.rs485_port.read()


        # def chain_scan(self):
        #     for address in range(255):
        #        self.write_to_serial(command=0x0,  data='Whois'.encode(), address=address)

    @staticmethod
    def wait_for_an_answer():
        GPIO.output(Communicator.en_tx_pin, 0)
        replay_buffer = Communicator.rs485_port.read(size=3)
        GPIO.output(Communicator.en_tx_pin, 1)
        usleep(800)
        return replay_buffer

    @staticmethod
    def delay_calculate(transmission):
        time_to_sleep = ((Communicator.bytesize + Communicator.stopbits + 1) / Communicator.baudrate) * len(
            transmission)
        time.sleep(time_to_sleep)


def msleep(ms):
    time.sleep(ms / 1000.0)

def usleep(us):
    time.sleep(us / 1000000.0)

