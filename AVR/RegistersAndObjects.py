import traceback
from AVR import Atmega16RegisterMap as BitMap
from AVR.Atmega16RegisterMap import Atmega16 as RegisterMap


class Register(object):

    def __init__(self, host):
        self.HOST = host
        self.VALUE = 0
        self.ADDRESS = None
        self.INSTANCE_NAME = None

        if self.INSTANCE_NAME is None:
            (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
            self.INSTANCE_NAME = text[:text.find('=')].strip()

        self.ADDRESS = RegisterMap[self.INSTANCE_NAME]

    def write(self, data):
        self.VALUE = data
        self.HOST.register_write(address=self.ADDRESS, value=self.VALUE)

    def read(self):
        self.VALUE = self.HOST.register_read(address=self.ADDRESS)
        return self.VALUE

    def set(self, data):
        self.VALUE |= data
        self.HOST.register_set(address=self.ADDRESS, value=data)

    def clear(self, data):
        self.VALUE &= ~data
        self.HOST.register_clear(address=self.ADDRESS, value=data)


class GPIO(object):

    def __init__(self, ddr, port, pin):
        self.DDR_REG = ddr
        self.PORT_REG = port
        self.PIN_REG = pin
        self.INSTANCE_NAME = None

        if self.INSTANCE_NAME is None:
            (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
            self.INSTANCE_NAME = text[:text.find('=')].strip()


class SPI(object):

    def __init__(self, spcr, spsr, spdr, spi_gpio):
        self.SPCR_REG = spcr
        self.SPSR_REG = spsr
        self.SPDR_REG = spdr
        self.SPI_PORT = spi_gpio

        self.MISO = BitMap.DDRB.DDB6
        self.MOSI = BitMap.DDRB.DDB5
        self.SS = BitMap.DDRB.DDB4
        self.SCK = BitMap.DDRB.DDB7
        self.SPE = BitMap.SPCR.SPE
        self.SPIE = BitMap.SPCR.SPIE
        self.DORD = BitMap.SPCR.DORD
        self.MSTR = BitMap.SPCR.MSTR
        self.SPR1 = BitMap.SPCR.SPR1
        self.SPR0 = BitMap.SPCR.SPR0
        self.CPOL = BitMap.SPCR.CPOL
        self.CPHA = BitMap.SPCR.CPHA

        self.SPI2X = BitMap.SPSR.SPI2X

        self.SPI_PORT.DDR_REG.clear(
            (1 << self.MOSI) |
            (1 << self.MISO) |
            (1 << self.SS) |
            (1 << self.SCK)
            )

        self.SPI_PORT.DDR_REG.set(
            (1 << self.MOSI) |
            (1 << self.MISO) |
            (1 << self.SS) |
            (1 << self.SCK)
        )

        self.SPCR_REG.write(
                (1 << self.SPE) |
                (0 << self.SPIE) |
                (0 << self.DORD) |
                (1 << self.MSTR) |
                (1 << self.SPR1) |
                (1 << self.SPR0) |
                (0 << self.CPOL) |
                (0 << self.CPHA)
                 )

        self.SPSR_REG.write(1 << self.SPI2X)
        self.SPI_PORT.PORT_REG.set(1 << self.SS)

    def select(self):
        self.SPI_PORT.PORT_REG.clear(1 << self.SS)

    def deselect(self):
        self.SPI_PORT.PORT_REG.set(1 << self.SS)

    def write_byte(self, data):
        self.SPDR_REG.write(data)


class ADC(object):

    def __init__(self, adch, adcl, adcsra, admux, acsr, adc_gpio, bitmap, vref=2.560):
        self.ADCH_REG = adch
        self.ADCL_REG = adcl
        self.ADCSRA_REG = adcsra
        self.ADMUX_REG = admux
        self.ACSR_REG = acsr
        self.ADC_GPIO = adc_gpio
        self.VREF = vref
        self.BITMAP = bitmap

        self.ADC_GPIO.DDR_REG.write(0x0)
        self.ADC_GPIO.PORT_REG.write(0x00)

        self.ADMUX_REG.write(
            (1 << self.BITMAP.ADMUX.REFS0) |
            (1 << self.BITMAP.ADMUX.REFS1)
            )  # internal Ref 2.56
        self.ADCSRA_REG.write(
            (1 << self.BITMAP.ADCSRA.ADEN) |
            (1 << self.BITMAP.ADCSRA.ADPS2) |
            (1 << self.BITMAP.ADCSRA.ADPS1) |
            (1 << self.BITMAP.ADCSRA.ADPS0)
            )

    def get_voltage(self, chanel, iterations=4):
        chanel &= 0x7   # of ‘CHANEL’ between 0 and 7
        self.ADMUX_REG.clear(
            (1 << self.BITMAP.ADMUX.MUX0) |
            (1 << self.BITMAP.ADMUX.MUX1) |
            (1 << self.BITMAP.ADMUX.MUX2)
            )
        self.ADMUX_REG.set(chanel)
        result = 0

        for iteration in range(0, iterations):
            self.ADCSRA_REG.set(1 << self.BITMAP.ADCSRA.ADSC)
            adcl = self.ADCL_REG.read()
            adch = self.ADCH_REG.read()
            result = result + (((adcl | (adch << 8)) / 0x3FF) * self.VREF)

        result = result / iterations

        return float(result)
