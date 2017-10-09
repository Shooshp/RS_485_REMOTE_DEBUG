from enum import IntEnum

class Atmega16(IntEnum):
    TWBR = 0x00
    TWSR = 0x01
    TWAR = 0x02
    TWDR = 0x03
    ADCL = 0x04
    ADCH = 0x05
    ADCSRA = 0x06
    ADMUX = 0x07
    ACSR = 0x08
    UBRRL = 0x09
    UCSRB = 0x0A
    UCSRA = 0x0B
    UDR = 0x0C
    SPCR = 0x0D
    SPSR = 0x0E
    SPDR = 0x0F
    PIND = 0x10
    DDRD = 0x11
    PORTD = 0x12
    PINC = 0x13
    DDRC = 0x14
    PORTC = 0x15
    PINB = 0x16
    DDRB = 0x17
    PORTB = 0x18
    PINA = 0x19
    DDRA = 0x1A
    PORTA = 0x1B
    EECR = 0x1C
    EEDR = 0x1D
    EEARL = 0x1E
    EEARH = 0x1F
    UBRRH = 0x20
    UCSRC = 0x20
    WDTCR = 0x21
    ASSR = 0x22
    OCR2 = 0x23
    TCNT2 = 0x24
    TCCR2 = 0x25
    ICR1L = 0x26
    ICR1H = 0x27
    OCR1BL = 0x28
    OCR1BH = 0x29
    OCR1AL = 0x2A
    OCR1AH = 0x2B
    TCNT1L = 0x2C
    TCNT1H = 0x2D
    TCCR1B = 0x2E
    TCCR1A = 0x2F
    SFIOR = 0x30
    OSCCAL = 0x31
    OCDR = 0x31
    TCNT0 = 0x32
    TCCR0 = 0x33
    MCUCSR = 0x34
    MCUCR = 0x35
    TWCR = 0x36
    SPMCSR = 0x37
    TIFR = 0x38
    TIMSK = 0x39
    GIFR = 0x3A
    GICR = 0x3B
    OCR0 = 0x3C

class TWBR(IntEnum):
    TWBR0  = 0
    TWBR1  = 1
    TWBR2  = 2
    TWBR3  = 3
    TWBR4  = 4
    TWBR5  = 5
    TWBR6  = 6
    TWBR7  = 7


class TWSR(IntEnum):
    TWPS0 = 0
    TWPS1 = 1
    TWS3  = 3
    TWS4  = 4
    TWS5  = 5
    TWS6  = 6
    TWS7  = 7

class TWAR(IntEnum):
    TWGCE = 0
    TWA0  = 1
    TWA1  = 2
    TWA2  = 3
    TWA3  = 4
    TWA4  = 5
    TWA5  = 6
    TWA6  = 7

class TWDR(IntEnum):
    TWD0  = 0
    TWD1  = 1
    TWD2  = 2
    TWD3  = 3
    TWD4  = 4
    TWD5  = 5
    TWD6  = 6
    TWD7  = 7

class ADCL(IntEnum):
    ADCL0  = 0
    ADCL1  = 1
    ADCL2  = 2
    ADCL3  = 3
    ADCL4  = 4
    ADCL5  = 5
    ADCL6  = 6
    ADCL7  = 7

class ADCH(IntEnum):
    ADCH0  = 0
    ADCH1  = 1
    ADCH2  = 2
    ADCH3  = 3
    ADCH4  = 4
    ADCH5  = 5
    ADCH6  = 6
    ADCH7  = 7

class ADCSRA(IntEnum):
    ADPS0 = 0
    ADPS1 = 1
    ADPS2 = 2
    ADIE  = 3
    ADIF  = 4
    ADATE = 5
    ADSC  = 6
    ADEN  = 7

class ADMUX(IntEnum):
    MUX0   = 0
    MUX1   = 1
    MUX2   = 2
    MUX3   = 3
    MUX4   = 4
    ADLAR  = 5
    REFS0  = 6
    REFS1  = 7

class ACSR(IntEnum):
    ACIS0 = 0
    ACIS1 = 1
    ACIC  = 2
    ACIE  = 3
    ACI   = 4
    ACO   = 5
    ACBG  = 6
    ACD   = 7

class UBRRL(IntEnum):
    UBRR0  = 0
    UBRR1  = 1
    UBRR2  = 2
    UBRR3  = 3
    UBRR4  = 4
    UBRR5  = 5
    UBRR6  = 6
    UBRR7  = 7

class UCSRB(IntEnum):
    TXB8   = 0
    RXB8   = 1
    UCSZ2  = 2
    TXEN   = 3
    RXEN   = 4
    UDRIE  = 5
    TXCIE  = 6
    RXCIE  = 7

class UCSRA(IntEnum):
    MPCM   = 0
    U2X    = 1
    UPE    = 2
    DOR    = 3
    FE     = 4
    UDRE   = 5
    TXC    = 6
    RXC    = 7

class UDR(IntEnum):
    UDR0  = 0
    UDR1  = 1
    UDR2  = 2
    UDR3  = 3
    UDR4  = 4
    UDR5  = 5
    UDR6  = 6
    UDR7  = 7

class SPCR(IntEnum):
    SPR0  = 0
    SPR1  = 1
    CPHA  = 2
    CPOL  = 3
    MSTR  = 4
    DORD  = 5
    SPE   = 6
    SPIE  = 7

class SPSR(IntEnum):
    SPI2X = 0
    WCOL  = 6
    SPIF  = 7

class SPDR(IntEnum):
    SPDR0  = 0
    SPDR1  = 1
    SPDR2  = 2
    SPDR3  = 3
    SPDR4  = 4
    SPDR5  = 5
    SPDR6  = 6
    SPDR7  = 7

class PIND(IntEnum):
    PIND0  = 0
    PIND1  = 1
    PIND2  = 2
    PIND3  = 3
    PIND4  = 4
    PIND5  = 5
    PIND6  = 6
    PIND7  = 7

class DDRD(IntEnum):
    DDD0  = 0
    DDD1  = 1
    DDD2  = 2
    DDD3  = 3
    DDD4  = 4
    DDD5  = 5
    DDD6  = 6
    DDD7  = 7

class PORTD(IntEnum):
    PORTD0  = 0
    PORTD1  = 1
    PORTD2  = 2
    PORTD3  = 3
    PORTD4  = 4
    PORTD5  = 5
    PORTD6  = 6
    PORTD7  = 7

class PINC(IntEnum):
    PINC0  = 0
    PINC1  = 1
    PINC2  = 2
    PINC3  = 3
    PINC4  = 4
    PINC5  = 5
    PINC6  = 6
    PINC7  = 7

class DDRC(IntEnum):
    DDC0  = 0
    DDC1  = 1
    DDC2  = 2
    DDC3  = 3
    DDC4  = 4
    DDC5  = 5
    DDC6  = 6
    DDC7  = 7

class PORTC(IntEnum):
    PORTC0  = 0
    PORTC1  = 1
    PORTC2  = 2
    PORTC3  = 3
    PORTC4  = 4
    PORTC5  = 5
    PORTC6  = 6
    PORTC7  = 7

class PINB(IntEnum):
    PINB0  = 0
    PINB1  = 1
    PINB2  = 2
    PINB3  = 3
    PINB4  = 4
    PINB5  = 5
    PINB6  = 6
    PINB7  = 7

class DDRB(IntEnum):
    DDB0  = 0
    DDB1  = 1
    DDB2  = 2
    DDB3  = 3
    DDB4  = 4
    DDB5  = 5
    DDB6  = 6
    DDB7  = 7

class PORTB(IntEnum):
    PORTB0  = 0
    PORTB1  = 1
    PORTB2  = 2
    PORTB3  = 3
    PORTB4  = 4
    PORTB5  = 5
    PORTB6  = 6
    PORTB7  = 7

class PINA(IntEnum):
    PINA0  = 0
    PINA1  = 1
    PINA2  = 2
    PINA3  = 3
    PINA4  = 4
    PINA5  = 5
    PINA6  = 6
    PINA7  = 7

class DDRA(IntEnum):
    DDA0  = 0
    DDA1  = 1
    DDA2  = 2
    DDA3  = 3
    DDA4  = 4
    DDA5  = 5
    DDA6  = 6
    DDA7  = 7

class PORTA(IntEnum):
    PORTA0  = 0
    PORTA1  = 1
    PORTA2  = 2
    PORTA3  = 3
    PORTA4  = 4
    PORTA5  = 5
    PORTA6  = 6
    PORTA7  = 7

class EECR(IntEnum):
    EERE = 0
    EEWE = 1
    EEMWE = 2
    EERIE  = 3

class EEDR(IntEnum):
    EEDR0  = 0
    EEDR1  = 1
    EEDR2  = 2
    EEDR3  = 3
    EEDR4  = 4
    EEDR5  = 5
    EEDR6  = 6
    EEDR7  = 7

class EEARL(IntEnum):
    EEAR0 = 0
    EEAR1 = 1
    EEAR2 = 2
    EEAR3  = 3
    EEAR4  = 4
    EEAR5  = 5
    EEAR6  = 6
    EEAR7  = 7

class EEARH(IntEnum):
    EEAR8 = 0

class UBRRH(IntEnum):
    UBRR8 = 0
    UBRR9 = 1
    UBRR10 = 2
    UBRR11  = 3

class UCSRC(IntEnum):
    UCPOL = 0
    UCSZ0 = 1
    UCSZ1 = 2
    USBS  = 3
    UPM0  = 4
    UPM1  = 5
    UMSEL  = 6
    URSEL  = 7

class WDTCR(IntEnum):
    WDP0 = 0
    WDP1 = 1
    WDP2 = 2
    WDE  = 3
    WDTOE  = 4

class ASSR(IntEnum):
    TCR2UB = 0
    OCR2UB = 1
    TCN2UB = 2
    AS2  = 3

class OCR2(IntEnum):
    OCR2_0 = 0
    OCR2_1 = 1
    OCR2_2 = 2
    OCR2_3  = 3
    OCR2_4  = 4
    OCR2_5  = 5
    OCR2_6  = 6
    OCR2_7  = 7

class TCNT2(IntEnum):
    TCNT2_0 = 0
    TCNT2_1 = 1
    TCNT2_2 = 2
    TCNT2_3  = 3
    TCNT2_4  = 4
    TCNT2_5  = 5
    TCNT2_6  = 6
    TCNT2_7  = 7

class TCCR2(IntEnum):
    CS20 = 0
    CS21 = 1
    CS22 = 2
    WGM21  = 3
    COM20  = 4
    COM21  = 5
    WGM20  = 6
    FOC2  = 7

class ICR1L(IntEnum):
    ICR1L0 = 0
    ICR1L1 = 1
    ICR1L2 = 2
    ICR1L3  = 3
    ICR1L4  = 4
    ICR1L5  = 5
    ICR1L6  = 6
    ICR1L7  = 7

class ICR1H(IntEnum):
    ICR1H0 = 0
    ICR1H1 = 1
    ICR1H2 = 2
    ICR1H3  = 3
    ICR1H4  = 4
    ICR1H5  = 5
    ICR1H6  = 6
    ICR1H7  = 7

class OCR1BL(IntEnum):
    OCR1BL0 = 0
    OCR1BL1 = 1
    OCR1BL2 = 2
    OCR1BL3  = 3
    OCR1BL4  = 4
    OCR1BL5  = 5
    OCR1BL6  = 6
    OCR1BL7  = 7

class OCR1BH(IntEnum):
    OCR1BH0 = 0
    OCR1BH1 = 1
    OCR1BH2 = 2
    OCR1BH3  = 3
    OCR1BH4  = 4
    OCR1BH5  = 5
    OCR1BH6  = 6
    OCR1BH7  = 7

class OCR1AL(IntEnum):
    OCR1AL0 = 0
    OCR1AL1 = 1
    OCR1AL2 = 2
    OCR1AL3  = 3
    OCR1AL4  = 4
    OCR1AL5  = 5
    OCR1AL6  = 6
    OCR1AL7  = 7

class OCR1AH(IntEnum):
    OCR1AH0 = 0
    OCR1AH1 = 1
    OCR1AH2 = 2
    OCR1AH3  = 3
    OCR1AH4  = 4
    OCR1AH5  = 5
    OCR1AH6  = 6
    OCR1AH7  = 7

class TCNT1L(IntEnum):
    TCNT1L0 = 0
    TCNT1L1 = 1
    TCNT1L2 = 2
    TCNT1L3  = 3
    TCNT1L4  = 4
    TCNT1L5  = 5
    TCNT1L6  = 6
    TCNT1L7  = 7

class TCNT1H(IntEnum):
    TCNT1H0 = 0
    TCNT1H1 = 1
    TCNT1H2 = 2
    TCNT1H3  = 3
    TCNT1H4  = 4
    TCNT1H5  = 5
    TCNT1H6  = 6
    TCNT1H7  = 7

class TCCR1B(IntEnum):
    CS10 = 0
    CS11 = 1
    CS12 = 2
    WGM12  = 3
    WGM13  = 4
    ICES1  = 6
    ICNC1  = 7

class TCCR1A(IntEnum):
    WGM10 = 0
    WGM11 = 1
    FOC1B = 2
    FOC1A  = 3
    COM1B0  = 4
    COM1B1  = 5
    COM1A0  = 6
    COM1A1  = 7

class SFIOR(IntEnum):
    PSR10 = 0
    PSR2 = 1
    PUD = 2
    ACME  = 3
    ADTS0  = 5
    ADTS1  = 6
    ADTS2  = 7

class OSCCAL(IntEnum):
    CAL0 = 0
    CAL1 = 1
    CAL2 = 2
    CAL3  = 3
    CAL4  = 4
    CAL5  = 5
    CAL6  = 6
    CAL7  = 7

class OCDR(IntEnum):
    OCDR0 = 0
    OCDR1 = 1
    OCDR2 = 2
    OCDR3  = 3
    OCDR4  = 4
    OCDR5  = 5
    OCDR6  = 6
    OCDR7  = 7

class TCNT0(IntEnum):
    TCNT0_0 = 0
    TCNT0_1 = 1
    TCNT0_2 = 2
    TCNT0_3  = 3
    TCNT0_4  = 4
    TCNT0_5  = 5
    TCNT0_6  = 6
    TCNT0_7  = 7

class TCCR0(IntEnum):
    CS00 = 0
    CS01 = 1
    CS02 = 2
    WGM01  = 3
    COM00  = 4
    COM01  = 5
    WGM00  = 6
    FOC0  = 7

class MCUCSR(IntEnum):
    PORF = 0
    EXTRF = 1
    BORF = 2
    WDRF  = 3
    JTRF  = 4
    ISC2  = 6
    JTD  = 7

class MCUCR(IntEnum):
    ISC00 = 0
    ISC01 = 1
    ISC10 = 2
    ISC11  = 3
    SM0  = 4
    SM1  = 5
    SE  = 6
    SM2  = 7

class TWCR(IntEnum):
    TWIE = 0
    TWEN = 2
    TWWC  = 3
    TWSTO  = 4
    TWSTA  = 5
    TWEA  = 6
    TWINT  = 7

class SPMCSR(IntEnum):
    SPMEN = 0
    PGERS = 1
    PGWRT = 2
    BLBSET  = 3
    RWWSRE  = 4
    RWWSB  = 6
    SPMIE  = 7

class TIFR(IntEnum):
    TOV0 = 0
    OCF0 = 1
    TOV1 = 2
    OCF1B  = 3
    OCF1A  = 4
    ICF1  = 5
    TOV2  = 6
    OCF2  = 7

class TIMSK(IntEnum):
    TOIE0 = 0
    OCIE0 = 1
    TOIE1 = 2
    OCIE1B  = 3
    OCIE1A  = 4
    TICIE1  = 5
    TOIE2  = 6
    OCIE2  = 7

class GIFR(IntEnum):
    INTF2  = 5
    INTF0  = 6
    INTF1  = 7

class GICR(IntEnum):
    IVCE = 0
    IVSEL = 1
    INT2  = 5
    INT0  = 6
    INT1  = 7

class OCR0(IntEnum):
    OCR0_0 = 0
    OCR0_1 = 1
    OCR0_2 = 2
    OCR0_3  = 3
    OCR0_4  = 4
    OCR0_5  = 5
    OCR0_6  = 6
    OCR0_7  = 7