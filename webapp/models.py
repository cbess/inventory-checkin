from core import peewee
from core import settings
from flask.ext import admin
from flask.ext.admin.contrib import peeweemodel
import sqlite3

INVENTORY_STATUS = [(1, 'Checkin'), (2, 'Checked out')]
db = peewee.SqliteDatabase(settings.DATABASE_NAME, check_same_thread=False)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Person(BaseModel):
    name = peewee.CharField(max_length=80)

    def __unicode__(self):
        return self.name


class User(Person):
    email = peewee.CharField(max_length=120)
    password = peewee.CharField(max_length=250)
    is_admin = peewee.BooleanField(default=False)

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __unicode__(self):
        return self.email


class InventoryItem(BaseModel):
    name = peewee.CharField(max_length=255)
    identifier = peewee.CharField(unique=True, null=True, max_length=500)
    comment = peewee.CharField(null=True, max_length=200)
    date_added = peewee.DateTimeField(null=True)
    date_updated = peewee.DateTimeField()
    status = peewee.IntegerField(default=1, choices=INVENTORY_STATUS)

    def __unicode__(self):
        return self.name


class InventoryLog(BaseModel):
    person = peewee.ForeignKeyField(Person, related_name='logs')
    item = peewee.ForeignKeyField(InventoryItem, related_name='logs')
    status = peewee.IntegerField(default=2, choices=INVENTORY_STATUS)
    date_added = peewee.DateTimeField()

    def __unicode__(self):
        return u'%s - %s' % (status, date_added)


def setup():
    tables = (User, InventoryItem, InventoryLog, Person)
    for table in tables:
        try:
            table.create_table()
            if User == table:
                # add an admin user
                User.insert(
                    name='admin',
                    email='admin@example.com',
                    password='admin',
                    is_admin=True
                ).execute()
                pass
        except sqlite3.OperationalError:
            # table may already exist
            pass
