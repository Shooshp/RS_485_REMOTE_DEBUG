import struct
import traceback
import time
import uuid
import numpy as np
from enum import IntEnum
from DataBase.ORMDataBase import devices_on_tester, power_source_calibration, power_source_measurement
from HostController import HostController, DevicePrefixes
from AVR import RegistersAndObjects
from AVR import Atmega16RegisterMap as BitMap
from AVR.ConnectedDevices.MCP4822 import MCP4822 as DAC


class PowerSourceCommands(IntEnum):
    register_write = 1
    register_read = 2
    register_set = 3
    register_clear = 4
    get_id = 5
    set_id = 6


class PowerSource(HostController):
    def __init__(self, address, communicator):

        super().__init__(communicator=communicator)
        if self.INSTANCE_NAME is None:
            (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
            self.INSTANCE_NAME = text[:text.find('=')].strip()

        if self.OBJECT_TYPE is None:
            self.OBJECT_TYPE = __class__.__name__

        if self.OBJECT_TYPE not in DevicePrefixes.__members__:
            raise Exception('Unknown device type: ' + str(self.OBJECT_TYPE))
        else:
            self.DEVICE_ADDRESS_PREFIX = DevicePrefixes[self.OBJECT_TYPE].value

        if address > 0xF or address < 0:
            raise Exception('Device addresses can only be in 0x0:0xF range! Get address of: ' + str(hex(address)))
        else:
            self.ADDRESS = self.DEVICE_ADDRESS_PREFIX | address

        self.CURRENT_LIMIT = 0
        self.VOLTAGE_SET = 0
        self.ZERO_ERROR = 0

        ADCL = RegistersAndObjects.Register(self)
        ADCH = RegistersAndObjects.Register(self)
        ADCSRA = RegistersAndObjects.Register(self)
        ADMUX = RegistersAndObjects.Register(self)
        ACSR = RegistersAndObjects.Register(self)
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

        self.GPIOA = RegistersAndObjects.GPIO(ddr=DDRA, port=PORTA, pin=PINA)
        self.GPIOB = RegistersAndObjects.GPIO(ddr=DDRB, port=PORTB, pin=PINB)
        self.GPIOC = RegistersAndObjects.GPIO(ddr=DDRC, port=PORTC, pin=PINC)
        self.GPIOD = RegistersAndObjects.GPIO(ddr=DDRD, port=PORTD, pin=PIND)

        if self.get_device_id():
            self.set_device_id()
            self.get_device_id()
            print('New device was detected, with address: ' + str(hex(self.ADDRESS)) + ' id was assigned: '
                  + str(self.DEVICE_ID))

        devices_on_tester.get_or_create(
            devices_on_tester_uuid = self.DEVICE_ID.hex(),
            devices_on_tester_type = str(self.OBJECT_TYPE)
        )

        self.SPI = RegistersAndObjects.SPI(
            spcr=SPCR,
            spsr=SPSR,
            spdr=SPDR,
            spi_gpio=self.GPIOB)
        self.DAC = DAC(
            spi_port=self.SPI,
            gpio_port=self.GPIOC,
            bitmap=BitMap)
        self.ADC = RegistersAndObjects.ADC(
            adch=ADCH,
            adcl=ADCL,
            adcsra=ADCSRA,
            admux=ADMUX,
            acsr=ACSR,
            adc_gpio=self.GPIOA,
            bitmap=BitMap)

        self.GPIOD.DDR_REG.set(1 << BitMap.PIND.PIND7)
        self.GPIOD.PORT_REG.set(1 << BitMap.PIND.PIND7)

        self.CALIBRATION_ID = self.OBJECT_TYPE + '_calibration_' + str(self.DEVICE_ID.hex())

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
        self.DEVICE_ID = bytearray()  # Clean this just in case
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

    def calibration(self):
        power_source_calibration.delete().where(
            power_source_calibration.power_source_calibration_uuid == self.DEVICE_ID.hex()).execute()

        results = []
        start = time.time()
        x = np.arange(0, 4.096, 0.001)
        y = np.array([])

        for value in x:
            self.DAC.set_voltage(0, value)
            read_voltage = self.ADC.get_voltage(0)
            results.append((float(value/2), read_voltage))
            y = np.append(y, read_voltage)
        end = time.time()
        self.DAC.clear()
        print('Calibration completed! Time to calibrate: ' + str((end - start)))

        calibration_func = np.polyfit(x, y, 1)
        polynomial = np.poly1d(calibration_func)

        x = np.arange(4.096, 5.120, 0.001)
        for value in x:
            results.append((float(value/2), float(polynomial(value))))

        for i in range(0, 5120):
            power_source_calibration.insert(
                power_source_calibration_uuid = self.DEVICE_ID.hex(),
                voltage_set = "%.4f" % results[i][0],
                voltage_get = "%.4f" % results[i][1]).execute()

    def get_zero_error(self):
        x = np.arange(0, 2.560, 0.0005)
        y = np.array([])

        for value in  power_source_calibration.select().where(
            power_source_calibration.power_source_calibration_uuid == self.DEVICE_ID.hex()).order_by(
            power_source_calibration.voltage_set.asc()
        ):
            temp = float(value.voltage_get)
            y = np.append(y,temp)

        calibration_func = np.polyfit(x, y, 1)
        self.ZERO_ERROR = calibration_func[1]

    def measure(self, chanel, division_coefficient):
        value = self.ADC.get_voltage(chanel=chanel, iterations=5)
        query = power_source_calibration.select(power_source_calibration.voltage_set).where(
            power_source_calibration.power_source_calibration_uuid == self.DEVICE_ID.hex() and
            ((power_source_calibration.voltage_get > value - 0.005) &
            (power_source_calibration.voltage_get < value + 0.005))).order_by(power_source_calibration.voltage_get.asc()).\
            limit(20).execute()

        result = []
        for value in query:
            result.append(value.voltage_set)

        return("%.4f" % ((sum(result)/len(result)) * division_coefficient))

    def measure_voltage(self):
        voltage = self.measure(chanel=3, division_coefficient=8)
        return voltage

    def measure_current(self):
        current = self.measure(chanel=2, division_coefficient=2)
        return current

    def measure_remperature(self):
        temperature = self.measure()

    def write_status_to_db(self):
        power_source_measurement.insert(
            power_source_measurement_uuid = self.DEVICE_ID.hex(),
            measurement_voltage = self.measure_voltage(),
            measurement_current = self.measure_current()
        ).execute()

    def set_voltage(self, voltage):
        self.VOLTAGE_SET = voltage
        self.DAC.set_voltage(chanel=0, data=0)
        value = ((self.VOLTAGE_SET - 0.1) / 4.97)
        self.DAC.set_voltage(chanel=0, data=value)
        self.turn_on()
        time.sleep(0.3)

        while ((self.VOLTAGE_SET+self.ZERO_ERROR) - float(self.measure_voltage())) > 0.005:
            value += 0.004
            self.DAC.set_voltage(chanel=0, data=value)
            time.sleep(0.1)

        while ((self.VOLTAGE_SET+self.ZERO_ERROR) - float(self.measure_voltage())) > 0.001:
            value += 0.001
            self.DAC.set_voltage(chanel=0, data=value)
            time.sleep(0.1)

    def set_current(self, current):
        self.CURRENT_LIMIT = current
        value = self.CURRENT_LIMIT * 1.3635
        self.DAC.set_voltage(chanel=1, data=value)

    def turn_off(self):
        self.GPIOD.PORT_REG.set(1 << BitMap.PIND.PIND7)

    def turn_on(self):
        self.GPIOD.PORT_REG.clear(1 << BitMap.PIND.PIND7)
