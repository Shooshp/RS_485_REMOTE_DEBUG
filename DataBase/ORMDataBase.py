from peewee import *
import peewee

db = peewee.MySQLDatabase(
    database='local_data_storage',
    host = 'localhost',
    user='admin',
    password='123' )

class MySQLModel(peewee.Model):
    class Meta:
        database = db

class device_index(MySQLModel):
    device_type_id = CharField(64, primary_key = True, null  = False, unique = True)
    address_prefix = IntegerField(null  = False, unique = True)

class devices_on_tester(MySQLModel):
    devices_on_tester_uuid = UUIDField(primary_key = True, null  = False, unique = True)
    devices_on_tester_type = ForeignKeyField(
        device_index,
        db_column='devices_on_tester_type',
        to_field='device_type_id')
    devices_on_tester_add_at = DateTimeField()

class power_source_calibration(MySQLModel):
    power_source_calibration_id = IntegerField(primary_key = True, null  = False, unique = True)
    power_source_calibration_uuid = ForeignKeyField(
        devices_on_tester,
        db_column='power_source_calibration_uuid',
        to_field='devices_on_tester_uuid')
    voltage_set = DecimalField(max_digits=6, decimal_places=4)
    voltage_get = DecimalField(max_digits=6, decimal_places=4)

class power_source_measurement(MySQLModel):
    power_source_measurement_id = IntegerField(primary_key = True, null  = False, unique = True)
    power_source_measurement_uuid = ForeignKeyField(
        devices_on_tester,
        db_column='power_source_measurement_uuid',
        to_field='devices_on_tester_uuid')
    measurement_voltage = DecimalField(max_digits=6, decimal_places=4)
    measurement_current = DecimalField(max_digits=6, decimal_places=4)
    measurement_temperature = DecimalField(max_digits=6, decimal_places=4)
    measured_at = DateTimeField()
