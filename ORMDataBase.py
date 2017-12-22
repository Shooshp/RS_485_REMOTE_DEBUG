from peewee import *
import peewee

db = peewee.MySQLDatabase(
    database='local_data_storage',
    host='localhost',
    user='admin',
    password='123')


class MySQLModel(peewee.Model):
    class Meta:
        database = db


class DeviceList(MySQLModel):
    Type = CharField(64, db_column='device_type_id', primary_key=True, null=False, unique=True)
    AddressPrefix = IntegerField(db_column='address_prefix', null=False, unique=True)

    class Meta:
        db_table = 'device_index'


class Devices(MySQLModel):
    UUID = CharField(40, db_column='devices_on_tester_uuid', primary_key=True, null=False, unique=True)
    Type = ForeignKeyField(
        DeviceList,
        db_column='devices_on_tester_type',
        to_field=DeviceList.Type)
    DateAdd = DateTimeField(db_column='devices_on_tester_add_at')
    Address = IntegerField(db_column='devices_on_tester_address', null=False, unique=True)

    class Meta:
        db_table = 'devices_on_tester'


class Calibration(MySQLModel):
    id = IntegerField(db_column='power_source_calibration_id', primary_key=True, null=False, unique=True)
    UUID = ForeignKeyField(
        Devices,
        db_column='power_source_calibration_uuid',
        to_field=Devices.UUID)
    VoltageSet = DecimalField(db_column='voltage_set', max_digits=6, decimal_places=4)
    VoltageGet = DecimalField(db_column='voltage_get', max_digits=6, decimal_places=4)
    CalibratedAt = DateTimeField(db_column='calibrated_at')

    class Meta:
        db_table = 'power_source_calibration'

    @staticmethod
    def clean_calibration(device_uuid):
        print("Cleaning calibration for: " + device_uuid)
        q = Calibration.delete().where(Calibration.UUID == device_uuid)
        result = q.execute()
        print("Calibration table was cleansed from " + device_uuid + " filth! " + result + " rows was purged." )

    @staticmethod
    def get_approximate_value_list(value, device_uuid):
        query = Calibration.select(Calibration.VoltageSet).where(
            Calibration.UUID == device_uuid and
            ((Calibration.VoltageGet > value - 0.005) &
             (Calibration.VoltageGet < value + 0.005))).order_by(
            Calibration.VoltageGet.asc()). \
            limit(20).execute()
        return query


class Measurement(MySQLModel):
    id = IntegerField(db_column='power_source_measurement_id', primary_key=True, null=False, unique=True)
    UUID = ForeignKeyField(
        Devices,
        db_column='power_source_measurement_uuid',
        to_field=Devices.UUID)
    Voltage = DecimalField(db_column='measurement_voltage', max_digits=6, decimal_places=4)
    Current = DecimalField(db_column='measurement_current', max_digits=6, decimal_places=4)
    Temperature = DecimalField(db_column='measurement_temperature', max_digits=6, decimal_places=4)
    Date = DateTimeField(db_column='measured_at')

    class Meta:
        db_table = 'power_source_measurement'


class Settings(MySQLModel):
    id = IntegerField(db_column='power_source_settings_id', primary_key=True, null=False, unique=True)
    UUID = ForeignKeyField(
        Devices,
        db_column='power_source_setting_uuid',
        to_field=Devices.UUID,
        related_name='SettingsUUID')

    Address = ForeignKeyField(
        Devices,
        db_column='power_source_settings_address',
        to_field=Devices.Address,
        related_name='SettingsAddress')

    SetVoltage = DecimalField(db_column='power_source_settings_voltage', max_digits=6, decimal_places=4)
    SetCurrent = DecimalField(db_column='power_source_settings_current', max_digits=6, decimal_places=4)
    SetPower = DecimalField(db_column='power_source_settings_power', max_digits=6, decimal_places=4)
    IsCalibrated = BooleanField(db_column='power_source_settings_calibration')
    IsOn = BooleanField(db_column='power_source_settings_on_off')

    class Meta:
        db_table = 'power_source_settings'


class TaskList(MySQLModel):
    id = IntegerField(db_column='power_source_task_list_id', primary_key=True, null=False, unique=True)
    Name = CharField(45, db_column='power_source_task_name', null=False)

    class Meta:
        db_table = 'power_source_task_list'


class CurrentTasks(MySQLModel):
    id = IntegerField(db_column='power_source_current_task_id', primary_key=True, null=False, unique=True)

    UUID = ForeignKeyField(
        Devices,
        db_column='power_source_current_task_device_uuid',
        to_field=Devices.UUID,
        related_name='CurrentTaskUUID')

    Name = ForeignKeyField(
        TaskList,
        db_column='power_source_current_task_name',
        to_field=TaskList.Name,
        related_name='CurrentTaskName')

    Value = DecimalField(db_column='power_source_current_task_argument', max_digits=6, decimal_places=4)
    IsCompleted = BooleanField(db_column='power_source_current_task_completed')
    BeginAt = DateTimeField(db_column='power_source_current_task_begin_at')

    class Meta:
        db_table = 'power_source_current_tasks'
