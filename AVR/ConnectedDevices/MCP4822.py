

class MCP4822(object):
    def __init__(self, spi_port, gpio_port, bitmap):
        self.SPI = spi_port
        self.LDAC = gpio_port
        self.BITMAP = bitmap
        self.VALUE = None

        self.LDAC.DDR_REG.set(1 << self.BITMAP.PINC.PINC6)
        self.LDAC.PORT_REG.set(1 << self.BITMAP.PINC.PINC6)

    def set_voltage(self, chanel, data):
        if chanel:
            self.VALUE = data | 0x9000
        else:
            self.VALUE = data | 0x1000

        self.SPI.select()
        self.SPI.write_byte(0xFF & (self.VALUE>>8))
        self.SPI.write_byte(0xFF & self.VALUE)
        self.SPI.deselect()

        self.LDAC.PORT_REG.clear(1 << self.BITMAP.PINC.PINC6)
        self.LDAC.PORT_REG.set(1 << self.BITMAP.PINC.PINC6)