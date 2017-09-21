import serial
import RPi.GPIO as GPIO

EN_485 = 12
EN_TX = 16

GPIO.setmode(GPIO.BOARD)
GPIO.setup(EN_485,GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(EN_TX,GPIO.OUT, initial=GPIO.HIGH)

ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

com = serial.Serial()

counter = 0

while 1:
    command = 'Write counter: %d ' % (counter)
    ser.write(command.encode())
    counter += 1
