import struct, time, traceback, uuid, numpy as np
from enum import IntEnum
from AVR import Atmega16RegisterMap as BitMap, RegistersAndObjects
from AVR.ConnectedDevices.MCP4822 import MCP4822 as DAC
from HostController import HostController, DevicePrefixes
from ORMDataBase import power_source_calibration, power_source_measurement, power_source_settings


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

        self.get_id()

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

        power_source_settings.get_or_create(
            power_source_setting_uuid = self.DEVICE_ID.hex(),
            power_source_settings_address = self.ADDRESS,
            power_source_settings_voltage = 12.435,
            power_source_settings_current = 1.0530,
            power_source_settings_power = 0,
            power_source_settings_calibration_set = 0,
            power_source_settings_on_off = False,
            power_source_settings_status = 2
        )
        self.VOLTAGE = 0
        self.CURRENT = 0
        self.POWER = 0
        self.IS_ON = 0

    def update_settings(self):
        settings = power_source_settings.select().where(power_source_setting_uuid = self.DEVICE_ID.hex())
        self.VOLTAGE = settings.power_source_settings_voltage
        self.CURRENT = settings.power_source_settings_current
        self.POWER = settings.power_source_settings_power

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

    def calibration(self):
        power_source_calibration.clean_calibration(self.DEVICE_ID)

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
        query = power_source_calibration.get_approximate_value_list(
            value=self.ADC.get_voltage(chanel=chanel, iterations=5),
            device_uuid=self.DEVICE_ID.hex())

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

    def measure_temperature(self):
        temperature = self.measure()
        return temperature

    def write_status_to_db(self):
        power_source_measurement.insert(
            power_source_measurement_uuid = self.DEVICE_ID.hex(),
            measurement_voltage = self.measure_voltage(),
            measurement_current = self.measure_current()
        ).execute()

    def set_voltage(self, voltage):
        self.VOLTAGE = voltage
        self.DAC.set_voltage(chanel=0, data=0)
        value = ((self.VOLTAGE - 0.1) / 4.97)
        self.DAC.set_voltage(chanel=0, data=value)
        self.turn_on()
        time.sleep(0.3)

        while ((self.VOLTAGE+self.ZERO_ERROR) - float(self.measure_voltage())) > 0.005:
            value += 0.004
            self.DAC.set_voltage(chanel=0, data=value)
            time.sleep(0.1)

        while ((self.VOLTAGE+self.ZERO_ERROR) - float(self.measure_voltage())) > 0.001:
            value += 0.001
            self.DAC.set_voltage(chanel=0, data=value)
            time.sleep(0.1)

    def set_current(self, current):
        self.CURRENT = current
        value = self.CURRENT * 1.3635
        self.DAC.set_voltage(chanel=1, data=value)

    def turn_off(self):
        self.IS_ON = False
        self.GPIOD.PORT_REG.set(1 << BitMap.PIND.PIND7)

    def turn_on(self):
        self.IS_ON = True
        self.GPIOD.PORT_REG.clear(1 << BitMap.PIND.PIND7)