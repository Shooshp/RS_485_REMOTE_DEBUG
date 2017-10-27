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

class device_types(MySQLModel):
    ID = IntegerField()
    TYPE = CharField()
    ADDRESS_PREFIX = IntegerField()

class power_source_calibration(MySQLModel):
    ID = IntegerField()
    UUID = CharField()
    V_SET = DecimalField()
    V_GET = DecimalField()