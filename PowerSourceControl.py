import struct
import traceback
import time
import uuid
from enum import IntEnum
from HostController import HostController, DevicePrefixes
from AVR import RegistersAndObjects
from AVR import  Atmega16RegisterMap as BitMap
from AVR.ConnectedDevices.MCP4822 import MCP4822 as DAC

class PowerSourceCommands(IntEnum):
    register_write = 1
    register_read = 2
    register_set = 3
    register_clear = 4
    get_id = 5
    set_id = 6

class PowerSource(HostController):
    def __init__(self, address, communicator, db_connector):

        super().__init__(communicator=communicator, db_connector=db_connector)
        if self.INSTANCE_NAME is None:
            (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
            self.INSTANCE_NAME = text[:text.find('=')].strip()

        if self.OBJECT_TYPE is None:
            self.OBJECT_TYPE = __class__.__name__

        if self.OBJECT_TYPE not in DevicePrefixes.__members__:
            raise Exception('Unknown device type: ' + str(self.OBJECT_TYPE))
        else:
            self.DEVICE_ADDRESS_PREFIX = DevicePrefixes[self.OBJECT_TYPE].value

        if  address > 0xF or address < 0 :
            raise Exception('Device addresses can only be in 0x0:0xF range! Get address of: ' + str(hex(address)))
        else:
            self.ADDRESS = self.DEVICE_ADDRESS_PREFIX | address


        self.CURRENT_LIMIT = 0
        self.VOLTAGE_SET = 0

        TWBR = RegistersAndObjects.Register(self)
        TWSR = RegistersAndObjects.Register(self)
        TWAR = RegistersAndObjects.Register(self)
        TWDR = RegistersAndObjects.Register(self)
        ADCL = RegistersAndObjects.Register(self)
        ADCH = RegistersAndObjects.Register(self)
        ADCSRA = RegistersAndObjects.Register(self)
        ADMUX = RegistersAndObjects.Register(self)
        ACSR = RegistersAndObjects.Register(self)
        UBRRL = RegistersAndObjects.Register(self)
        UCSRB = RegistersAndObjects.Register(self)
        UCSRA = RegistersAndObjects.Register(self)
        UDR = RegistersAndObjects.Register(self)
        SPCR = RegistersAndObjects.Register(self)
        SPSR = RegistersAndObjects.Register(self)
        SPDR = RegistersAndObjects.Register(self)
        PIND = RegistersAndObjects.Register(self)
        DDRD = RegistersAndObjects.Register(self)
        PORTD = RegistersAndObjects.Register(self)
        PINC = RegistersAndObjects.Register(self)
        DDRC = RegistersAndObjects.Register(self)
        PORTC = RegistersAndObjects.Register(self)
        PINB = RegistersAndObjects.Register(self)
        DDRB = RegistersAndObjects.Register(self)
        PORTB = RegistersAndObjects.Register(self)
        PINA = RegistersAndObjects.Register(self)
        DDRA = RegistersAndObjects.Register(self)
        PORTA = RegistersAndObjects.Register(self)
        EECR = RegistersAndObjects.Register(self)
        EEDR = RegistersAndObjects.Register(self)
        EEARL = RegistersAndObjects.Register(self)
        EEARH = RegistersAndObjects.Register(self)
        UBRRH = RegistersAndObjects.Register(self)
        UCSRC = RegistersAndObjects.Register(self)
        WDTCR = RegistersAndObjects.Register(self)
        ASSR = RegistersAndObjects.Register(self)
        OCR2 = RegistersAndObjects.Register(self)
        TCNT2 = RegistersAndObjects.Register(self)
        TCCR2 = RegistersAndObjects.Register(self)
        ICR1L = RegistersAndObjects.Register(self)
        ICR1H = RegistersAndObjects.Register(self)
        OCR1BL = RegistersAndObjects.Register(self)
        OCR1BH = RegistersAndObjects.Register(self)
        OCR1AL = RegistersAndObjects.Register(self)
        OCR1AH = RegistersAndObjects.Register(self)
        TCNT1L = RegistersAndObjects.Register(self)
        TCNT1H = RegistersAndObjects.Register(self)
        TCCR1B = RegistersAndObjects.Register(self)
        TCCR1A = RegistersAndObjects.Register(self)
        SFIOR = RegistersAndObjects.Register(self)
        OSCCAL = RegistersAndObjects.Register(self)
        OCDR = RegistersAndObjects.Register(self)
        TCNT0 = RegistersAndObjects.Register(self)
        TCCR0 = RegistersAndObjects.Register(self)
        MCUCSR = RegistersAndObjects.Register(self)
        MCUCR = RegistersAndObjects.Register(self)
        TWCR = RegistersAndObjects.Register(self)
        SPMCSR = RegistersAndObjects.Register(self)
        TIFR = RegistersAndObjects.Register(self)
        TIMSK = RegistersAndObjects.Register(self)
        GIFR = RegistersAndObjects.Register(self)
        GICR = RegistersAndObjects.Register(self)
        OCR0 = RegistersAndObjects.Register(self)

        self.GPIOA = RegistersAndObjects.GPIO(DDRA, PORTA, PINA)
        self.GPIOB = RegistersAndObjects.GPIO(DDRB, PORTB, PINB)
        self.GPIOC = RegistersAndObjects.GPIO(DDRC, PORTC, PINC)
        self.GPIOD = RegistersAndObjects.GPIO(DDRD, PORTD, PIND)

        if self.get_device_id():
            self.set_device_id()
            self.get_device_id()
            print('New device was detected, with address: ' + str(hex(self.ADDRESS)) + ' id was assigned: '
                  + str(self.DEVICE_ID))

        self.SPI = RegistersAndObjects.SPI(SPCR,SPSR,SPDR,self.GPIOB)
        self.DAC = DAC(spi_port=self.SPI, gpio_port=self.GPIOC, bitmap=BitMap)
        self.ADC = RegistersAndObjects.ADC(ADCH,ADCL,ADCSRA,ADMUX,ACSR,self.GPIOA, BitMap)

        self.get_device_id()
        self.CALIBRATION_TABLE_NAME = self.OBJECT_TYPE + '_calibration_' + str(self.DEVICE_ID.hex())

    def register_write(self, address, value):
        self.ARRAY_TO_SEND = struct.pack('>HB', address, value)
        self.COMMAND = PowerSourceCommands.register_write
        self.write()

    def register_read(self, address):
        self.ARRAY_TO_SEND = struct.pack('>H', address)
        self.COMMAND = PowerSourceCommands.register_read
        self.read()
        return self.ARRAY_TO_RECEIVE

    def register_set(self, address, value):
        self.ARRAY_TO_SEND = struct.pack('>HB', address, value)
        self.COMMAND = PowerSourceCommands.register_set
        self.write()

    def register_clear(self, address, value):
        self.ARRAY_TO_SEND = struct.pack('>HB', address, value)
        self.COMMAND = PowerSourceCommands.register_clear
        self.write()

    def get_device_id(self):
        self.DEVICE_ID = bytearray() #Clean this just in case
        status = 0
        for device_id_byte in range(0, 16):
            self.ARRAY_TO_SEND = struct.pack('>H', device_id_byte)
            self.COMMAND = PowerSourceCommands.get_id
            self.read()
            self.DEVICE_ID = self.DEVICE_ID + bytes([self.ARRAY_TO_RECEIVE])
            if self.ARRAY_TO_RECEIVE == 0xFF:
                status += 1
        if status != 16:
            status = 0
        return status

    def set_device_id(self):
        unique_id = uuid.uuid4()
        for device_id_byte in range(0, 16):
            self.ARRAY_TO_SEND = struct.pack('>HB', device_id_byte, unique_id.bytes[device_id_byte])
            self.COMMAND = PowerSourceCommands.set_id
            self.write()
            time.sleep(0.01)

    def clear_device_id(self):
        for device_id_byte in range(0, 16):
            self.ARRAY_TO_SEND = struct.pack('>HB', device_id_byte, 0xFF)
            self.COMMAND = PowerSourceCommands.set_id
            self.write()
            time.sleep(0.01)

    def calibration(self, force = None):
        self.DB_CONNECTOR.open_connection_to_db('local_data_storage')
        self.DB_CONNECTOR.cursor_create()

        self.DB_CONNECTOR.CURSOR.execute('DROP TABLE IF EXISTS ' + self.CALIBRATION_TABLE_NAME)
        self.DB_CONNECTOR.CONNECTOR.commit()
        self.DB_CONNECTOR.CURSOR.execute('CREATE TABLE '+self.CALIBRATION_TABLE_NAME+' (V_SET INT(1),V_GET INT(1))')
        self.DB_CONNECTOR.CONNECTOR.commit()


        results = []
        start = time.time()
        for value in range(0, 4096):
            self.DAC.set_voltage(0,value)
            read_voltage = self.ADC.get_voltage(0)*2
            results.append((value,read_voltage))
        end = time.time()
        print('Calibration completed! Time to calibrate: ' + str((end - start)))

        query = 'INSERT INTO '+self.CALIBRATION_TABLE_NAME+'(V_SET,V_GET)' \
                'VALUES(%s,%s)'

        self.DB_CONNECTOR.CURSOR.executemany(query, results)
        self.DB_CONNECTOR.CONNECTOR.commit()

        self.DB_CONNECTOR.cursor_kill()
        self.DB_CONNECTOR.close_connection_to_db()
        print(results)
