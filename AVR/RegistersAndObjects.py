import traceback
from AVR.AVR_SPI import Atmega16 as RegisterMap


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

        print('Register ' + str(self.INSTANCE_NAME) + ' init with address of ' + str(hex(self.ADDRESS)))

    def write(self, data):
        self.VALUE = data
        self.HOST.write_to_register(self.ADDRESS, self.VALUE)

    def read(self):
        return self.VALUE


class GPIO(object):

    def __init__(self, ddr, port, pin):
        self.DDR_REG = ddr
        self.PORT_REG = port
        self.PIN_REG = pin
        self.INSTANCE_NAME = None

        if self.INSTANCE_NAME is None:
            (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
            self.INSTANCE_NAME = text[:text.find('=')].strip()

    def ddr(self, value = None):
        if value is None:
            return self.DDR_REG.read()
        else:
            self.DDR_REG.write(value)

    def port(self, value = None):
        if value is None:
            return self.PORT_REG.read()
        else:
            self.PORT_REG.write(value)

    def pin(self, value = None):
        if value is None:
            return self.PIN_REG.read()
        else:
            self.PIN_REG.write(value)


class SPI(object):

    def __init__(self, spcr, spsr, spdr):
        self.SPCR_REG = spcr
        self.SPSR_REG = spsr
        self.SPDR_REG = spdr

    def spcr(self, value=None):
        if value is None:
            return self.SPCR_REG.read()
        else:
            self.SPCR_REG.write(value)

    def spsr(self, value=None):
        if value is None:
            return self.SPSR_REG.read()
        else:
            self.SPSR_REG.write(value)

    def spdr(self, value=None):
        if value is None:
            return self.SPDR_REG.read()
        else:
            self.SPDR_REG.write(value)

class ADC(object):

    def __init__(self, adch, adcl, adcsra, admux, acsr, adcgpio, vref = 2.56):
        self.ADCH_REG = adch
        self.ADCL_REG = adcl
        self.ADCSRA_REG = adcsra
        self.ADMUX_REG = admux
        self.ACSR_REG = acsr

        self.ADC_GPIO_PORT = adcgpio

        self.VREF = vref

        self.ADC_GPIO_PORT.ddr(0x0)
        self.ADC_GPIO_PORT.port(0x0)
        self.admux(0xC0) #internal Ref 2.56
        self.adcsra()

    def adch(self, value=None):
        if value is None:
            return self.ADCH_REG.read()
        else:
            self.ADCH_REG.write(value)

    def adcl(self, value=None):
        if value is None:
            return self.ADCL_REG.read()
        else:
            self.ADCL_REG.write(value)

    def adcsra(self, value=None):
        if value is None:
            return self.ADCSRA_REG.read()
        else:
            self.ADCSRA_REG.write(value)

    def admux(self, value=None):
        if value is None:
            return self.ADMUX_REG.read()
        else:
            self.ADMUX_REG.write(value)

    def acsr(self, value=None):
        if value is None:
            return self.ACSR_REG.read()
        else:
            self.ACSR_REG.write(value)



