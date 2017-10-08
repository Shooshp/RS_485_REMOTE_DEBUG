import struct
import traceback
from HostController import HostController
from AVR.AVR_SPI import Atmega16 as RegisterMap
from enum import IntEnum
from AVR import RegistersAndObjects


class PowerSourceCommands(IntEnum):
    set_voltage = 1
    set_current = 2
    set_alarm_fringe = 3
    read_voltage = 4
    read_current = 5
    read_temperature = 6
    turn_on = 7
    turn_off = 8

    register_write = 20
    register_read = 21


class PowerSource(HostController):
    def __init__(self, address):

        super().__init__(address=address)
        if self.INSTANCE_NAME is None:
            (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
            self.INSTANCE_NAME = text[:text.find('=')].strip()

        if self.OBJECT_TYPE is None:
            self.OBJECT_TYPE = __class__.__name__

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

        self.GPIOA.ddr(0x1)


    def set_voltage(self, value):
        is_int = isinstance(value, int)

        if not is_int:
            raise Exception("Please provide integer value for set_voltage() function")

        self.VOLTAGE_SET = value

        if self.VOLTAGE_SET > 20000:
            self.VOLTAGE_SET = 20000

        if self.VOLTAGE_SET < 0:
            self.VOLTAGE_SET = 0

        self.ARRAY_TO_SEND = struct.pack('>H', self.VOLTAGE_SET)
        self.COMMAND = PowerSourceCommands.set_voltage
        self.write(self)

    def set_current(self, value):
        is_int = isinstance(value, int)

        if not is_int:
            raise Exception("Please provide integer value for set_current() function")

        if self.CURRENT_LIMIT > 3000:
            self.CURRENT_LIMIT = 3000

        if self.CURRENT_LIMIT < 0:
            self.CURRENT_LIMIT = 0

        self.ARRAY_TO_SEND = struct.pack('>H', self.CURRENT_LIMIT)
        self.COMMAND = PowerSourceCommands.set_current
        self.write(self)

    def write_to_register(self, address, value):
        self.ARRAY_TO_SEND = struct.pack('>HB', address, value)
        self.COMMAND = PowerSourceCommands.register_write
        #self.write()
        print(self.ARRAY_TO_SEND)

    def read_from_register(self, address):
        self.ARRAY_TO_SEND = struct.pack('>H', address)
        self.COMMAND = PowerSourceCommands.register_read
        data = self.read(self)
        return data


