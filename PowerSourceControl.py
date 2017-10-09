import struct
import traceback
from enum import IntEnum
from HostController import HostController
from AVR import RegistersAndObjects
from AVR import  Atmega16RegisterMap as BitMap
from AVR.Atmega16RegisterMap import Atmega16 as RegisterMap
from AVR.ConnectedDevices.MCP4822 import MCP4822 as DAC




class PowerSourceCommands(IntEnum):
    register_write = 1
    register_read = 2
    register_set = 3
    register_clear = 4



class PowerSource(HostController):
    def __init__(self, address, communicator):

        super().__init__(address=address, communicator=communicator)
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

        self.SPI = RegistersAndObjects.SPI(SPCR,SPSR,SPDR,self.GPIOB)

        self.DAC = DAC(spi_port=self.SPI, gpio_port=self.GPIOC, bitmap=BitMap)

        self.ADC = RegistersAndObjects.ADC(ADCH,ADCL,ADCSRA,ADMUX,ACSR,self.GPIOA, BitMap)


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


