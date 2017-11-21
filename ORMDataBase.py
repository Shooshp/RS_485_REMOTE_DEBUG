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


class device_index(MySQLModel):
    device_type_id = CharField(64, primary_key=True, null=False, unique=True)
    address_prefix = IntegerField(null=False, unique=True)


class devices_on_tester(MySQLModel):
    devices_on_tester_uuid = UUIDField(primary_key=True, null=False, unique=True)
    devices_on_tester_type = ForeignKeyField(
        device_index,
        db_column='devices_on_tester_type',
        to_field='device_type_id')
    devices_on_tester_add_at = DateTimeField()
    devices_on_tester_address = IntegerField(null=False, unique=True)


class power_source_calibration(MySQLModel):
    power_source_calibration_id = IntegerField(primary_key=True, null=False, unique=True)
    power_source_calibration_uuid = ForeignKeyField(
        devices_on_tester,
        db_column='power_source_calibration_uuid',
        to_field='devices_on_tester_uuid')
    voltage_set = DecimalField(max_digits=6, decimal_places=4)
    voltage_get = DecimalField(max_digits=6, decimal_places=4)

    @staticmethod
    def clean_calibration(device_uuid):
        power_source_calibration.delete().where(
            power_source_calibration.power_source_calibration_uuid == device_uuid).execute()

    @staticmethod
    def get_approximate_value_list(value, device_uuid):
        query = power_source_calibration.select(power_source_calibration.voltage_set).where(
            power_source_calibration.power_source_calibration_uuid == device_uuid and
            ((power_source_calibration.voltage_get > value - 0.005) &
             (power_source_calibration.voltage_get < value + 0.005))).order_by(
            power_source_calibration.voltage_get.asc()). \
            limit(20).execute()
        return query


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


class power_source_settings(MySQLModel):
    power_source_settings_id = IntegerField(primary_key=True, null=False, unique=True)

    power_source_setting_uuid = ForeignKeyField(
        devices_on_tester,
        db_column='power_source_setting_uuid',
        to_field='devices_on_tester_uuid',
        related_name='uuid')

    power_source_settings_address = ForeignKeyField(
        devices_on_tester,
        db_column='power_source_settings_address',
        to_field='devices_on_tester_address',
        related_name='address')

    power_source_settings_voltage = DecimalField(max_digits=6, decimal_places=4)
    power_source_settings_current = DecimalField(max_digits=6, decimal_places=4)
    power_source_settings_power = DecimalField(max_digits=6, decimal_places=4)
    power_source_settings_calibration = BooleanField()
    power_source_settings_on_off = BooleanField()



class power_source_task_list(MySQLModel):
    power_source_task_list_id = IntegerField(primary_key=True, null=False, unique=True)
    power_source_task_name = CharField(45, null=False)


class power_source_current_tasks(MySQLModel):
    power_source_current_task_id = IntegerField(primary_key=True, null=False, unique=True)

    power_source_current_task_device_uuid = ForeignKeyField(
        devices_on_tester,
        db_column='power_source_current_task_device_uuid',
        to_field='devices_on_tester_uuid')

    power_source_current_task_name = ForeignKeyField(
        power_source_task_list,
        db_column='power_source_current_task_name',
        to_field='power_source_task_name')

    power_source_current_task_argument = DecimalField(max_digits=6, decimal_places=4)
    power_source_current_task_completed = BooleanField()
    power_source_current_task_begin_at = DateTimeField()
