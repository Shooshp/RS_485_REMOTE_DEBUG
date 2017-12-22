import numpy as np
import struct
import time
import traceback
from enum import IntEnum
import MorseParser

from AVR import Atmega16RegisterMap as BitMap, RegistersAndObjects
from AVR.ConnectedDevices.MCP4822 import MCP4822 as DAC
from HostController import HostController, DevicePrefixes
from ORMDataBase import Calibration, Measurement, Settings


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

        # onof controll
        self.GPIOD.DDR_REG.set(1 << BitMap.PIND.PIND7)
        self.GPIOD.PORT_REG.set(1 << BitMap.PIND.PIND7)

        # manual protection
        self.GPIOC.DDR_REG.set(1 << BitMap.PINC.PINC7)
        self.GPIOC.PORT_REG.clear(1 << BitMap.PINC.PINC7)

        # reset protection
        self.GPIOD.DDR_REG.set(1 << BitMap.PIND.PIND6)
        self.GPIOD.PORT_REG.clear(1 << BitMap.PIND.PIND6)

        # beeper
        self.GPIOD.DDR_REG.set(1 << BitMap.PIND.PIND5)
        self.GPIOD.PORT_REG.clear(1 << BitMap.PIND.PIND5)

        calibration_entries = Calibration.select(). \
            where(Calibration.UUID == self.DEVICE_ID.hex()).count()

        self.isCalibrated = False
        if calibration_entries == 5120:
            self.isCalibrated = True

        self.VOLTAGE = 0
        self.CURRENT = 0
        self.POWER = 0
        self.IS_ON = False

        Settings.get_or_create(
            UUID=self.DEVICE_ID.hex(),
            Address=self.ADDRESS)

        self.update_settings()
        self.beep()
        # self.get_zero_error()

    def update_settings(self):
        query = Settings.update(
            SetVoltage=self.VOLTAGE,
            SetCurrent=self.CURRENT,
            SetPower=self.POWER,
            IsCalibrated=self.isCalibrated,
            IsOn=self.IS_ON
        ).where(Settings.UUID == self.DEVICE_ID.hex())
        query.execute()

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
        Calibration.clean_calibration(self.DEVICE_ID.hex())

        results = []
        start = time.time()
        x = np.arange(0, 4.096, 0.001)
        y = np.array([])

        for value in x:
            self.DAC.set_voltage(0, value)
            read_voltage = self.ADC.get_voltage(0)
            results.append((float(value / 2), read_voltage))
            y = np.append(y, read_voltage)
        end = time.time()
        self.DAC.clear()
        print('Calibration completed! Time to calibrate: ' + str((end - start)))

        calibration_func = np.polyfit(x, y, 1)
        polynomial = np.poly1d(calibration_func)

        x = np.arange(4.096, 5.120, 0.001)
        for value in x:
            results.append((float(value / 2), float(polynomial(value))))

        for i in range(0, 5120):
            Calibration.insert(
                UUID=self.DEVICE_ID.hex(),
                VoltageSet="%.4f" % results[i][0],
                VoltageGet="%.4f" % results[i][1]).execute()

        self.isCalibrated = True
        self.update_settings()

    def get_zero_error(self):
        x = np.arange(0, 2.560, 0.0005)
        y = np.array([])

        for value in Calibration.select().where(
                Calibration.UUID == self.DEVICE_ID.hex()).order_by(
            Calibration.VoltageSet.asc()
        ):
            temp = float(value.VoltageSet)
            y = np.append(y, temp)

        calibration_func = np.polyfit(x, y, 1)
        self.ZERO_ERROR = calibration_func[1]

    def measure(self, chanel, division_coefficient):
        query = Calibration.get_approximate_value_list(
            value=self.ADC.get_voltage(chanel=chanel, iterations=5),
            device_uuid=self.DEVICE_ID.hex())

        result = []
        for value in query:
            result.append(value.VoltageSet)

        return "%.4f" % ((sum(result) / len(result)) * division_coefficient)

    def measure_voltage(self):
        voltage = self.measure(chanel=3, division_coefficient=8)
        return voltage

    def measure_current(self):
        current = self.measure(chanel=2, division_coefficient=2)
        return current

    # def measure_temperature(self):
    # temperature = self.measure()
    # return temperature

    def write_status_to_db(self):
        Measurement.insert(
            UUID=self.DEVICE_ID.hex(),
            Voltage=self.measure_voltage(),
            Current=self.measure_current()
        ).execute()

    def set_voltage(self, voltage):
        if voltage > 20:
            self.VOLTAGE = 20
        if voltage < 0:
            self.VOLTAGE = 0

        self.VOLTAGE = voltage
        self.update_settings()

        self.turn_off()
        time.sleep(0.3)
        kill_time = time.time()
        while ((time.time() - kill_time) < 20) and (float(self.measure_voltage()) > float(self.VOLTAGE) * 0.1):
            time.sleep(0.01)

        self.DAC.set_voltage(chanel=0, data=0)
        time.sleep(0.3)
        self.GPIOD.PORT_REG.clear(1 << BitMap.PIND.PIND7)
        time.sleep(0.3)

        steps = []

        start_set_procedure = time.time()

        while ((time.time() - start_set_procedure) < 20) and ((float(self.VOLTAGE) - float(self.measure_voltage())) > 0.04):
            difference = round((float(self.VOLTAGE) - float(self.measure_voltage())), 3)
            print('Dif: ', difference)

            steps.clear()

            for step in range(1, 5):
                steps.append(round(float(self.VOLTAGE) - difference + (difference * (step * 0.2)), 3))

            for step in steps:
                print('Step ', step)
                value = step / 4.97
                self.DAC.set_voltage(chanel=0, data=value)
                intermediate_voltage = self.measure_voltage()

                start = time.time()
                while ((time.time() - start) < 2) and ((float(intermediate_voltage) - float(self.measure_voltage())) > 0.04):
                    intermediate_voltage = self.measure_voltage()
                    print('Time: ', time.time() - start)
                    print('Set step ', step, ' Voltage ', intermediate_voltage)

        self.turn_on()

    def set_current(self, current):
        self.CURRENT = current
        self.update_settings()
        value = self.CURRENT * 1.3635
        self.DAC.set_voltage(chanel=1, data=value)

    def reset_protection(self):
        self.GPIOD.PORT_REG.set(1 << BitMap.PIND.PIND6)
        time.sleep(0.1)
        self.GPIOD.PORT_REG.clear(1 << BitMap.PIND.PIND6)

    def turn_off(self):
        self.GPIOD.PORT_REG.set(1 << BitMap.PIND.PIND7)
        self.IS_ON = False
        self.update_settings()

    def turn_on(self):
        self.GPIOD.PORT_REG.clear(1 << BitMap.PIND.PIND7)
        time.sleep(0.1)
        self.reset_protection()
        self.IS_ON = True
        self.update_settings()
        self.morse_beep('Online')

    def beep(self):
        self.GPIOD.PORT_REG.set(1 << BitMap.PIND.PIND5)
        self.GPIOD.PORT_REG.clear(1 << BitMap.PIND.PIND5)

    def morse_beep(self, text):
        result = MorseParser.MorseParser(text)

        for char in result:
            if char == ".":
                self.GPIOD.PORT_REG.set(1 << BitMap.PIND.PIND5)
                time.sleep(0.05)
                self.GPIOD.PORT_REG.clear(1 << BitMap.PIND.PIND5)
                time.sleep(0.05)
            if char == "-":
                self.GPIOD.PORT_REG.set(1 << BitMap.PIND.PIND5)
                time.sleep(0.150)
                self.GPIOD.PORT_REG.clear(1 << BitMap.PIND.PIND5)
                time.sleep(0.05)

            if char == " ":
                self.GPIOD.PORT_REG.clear(1 << BitMap.PIND.PIND5)
                time.sleep(0.150)

            if char == "_":
                self.GPIOD.PORT_REG.clear(1 << BitMap.PIND.PIND5)
                time.sleep(0.35)
