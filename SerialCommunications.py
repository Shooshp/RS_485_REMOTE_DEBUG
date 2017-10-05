import serial
import time
import RPi.GPIO as GPIO
import struct
from HostController import HostController
from PowerSourceControl import PowerSource
from PyCRC.CRC16 import CRC16

class Communicator(object):

    port = '/dev/ttyS0'
    baudrate = 1000000
    parity = serial.PARITY_NONE
    stopbits = serial.STOPBITS_ONE
    bytesize = serial.EIGHTBITS
    timeout = 0.1
    en_485_pin = 12
    en_tx_pin = 16
    crc_constant = 0xA001
    CURRENT_CRC = int()
    BUFFER_ARRAY = bytearray()
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

        usleep = lambda x: time.sleep(x / 1000000.0)
        msleep = lambda x: time.sleep(x / 1000.0)

        msleep(5)

    @staticmethod
    def write_to_serial(host):
        Communicator.HOST = host

        status = 0
        error_counter = 0

        while not status and error_counter < 100:
            Communicator.enclose()
            Communicator.rs485_port.write(Communicator.BUFFER_ARRAY)
            # print('Full Message: ' + str(self.BUFFER_ARRAY))
            Communicator.delay_calculate(Communicator.BUFFER_ARRAY)

            callback = Communicator.wait_for_an_answer()

            if callback:
                if struct.unpack('B', callback[0:1])[0] == Communicator.HOST.ADDRESS and \
                                struct.unpack('>H', callback[1:3])[0] == Communicator.CURRENT_CRC:
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

            print('Data was successfully send to host '
                  + str(Communicator.HOST.OBJECT_TYPE)   + ': '
                  + str(Communicator.HOST.INSTANCE_NAME) + ' at address '
                  + str(hex(Communicator.HOST.ADDRESS))  + '!'
                  + error_message)

        else:
            print('Failed to reach host '
                  + str(Communicator.HOST.OBJECT_TYPE)   + ': '
                  + str(Communicator.HOST.INSTANCE_NAME) + ' at address '
                  + str(hex(Communicator.HOST.ADDRESS))  + '!')

    @staticmethod
    def read_from_serial():
        Communicator.rs485_port.read()

    @staticmethod
    def enclose():
        data_length = len(Communicator.HOST.ARRAY_TO_SEND)


        Communicator.BUFFER_ARRAY = struct.pack('BBB', Communicator.HOST.ADDRESS, Communicator.HOST.COMMAND, data_length) \
                                    + Communicator.HOST.ARRAY_TO_SEND
        Communicator.CURRENT_CRC  = CRC16().calculate(Communicator.BUFFER_ARRAY)
        Communicator.BUFFER_ARRAY = Communicator.BUFFER_ARRAY + struct.pack('>H', Communicator.CURRENT_CRC)


   # def chain_scan(self):
   #     for address in range(255):
   #        self.write_to_serial(command=0x0,  data='Whois'.encode(), address=address)

    @staticmethod
    def wait_for_an_answer():
        GPIO.output(Communicator.en_tx_pin, 0)
        replay_buffer = Communicator.rs485_port.read(size=3)
        GPIO.output(Communicator.en_tx_pin, 1)
        #print('Got Replay: ' + str(replay_buffer))
        return replay_buffer

    @staticmethod
    def delay_calculate(transmission):
        time_to_sleep = ((Communicator.bytesize + Communicator.stopbits + 1) / Communicator.baudrate) * len(transmission)
        time.sleep(time_to_sleep)



