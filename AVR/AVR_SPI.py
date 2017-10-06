from AVR import Atmega16RegisterMap as Atmega16

class AVR_SPI(object):
    spi_port = Atmega16.PORTB
    spi_ddr  = Atmega16.DDRB

    spi_ddr_MISO = Atmega16.DDB6
    spi_ddr_MOSI = Atmega16.DDB5
    spi_ddr_SS   = Atmega16.DDB4
    spi_ddr_CLK  = Atmega16.DDB7

    spi_pin_SS = Atmega16.PINB4

