from core import peewee
from core import settings
from flask.ext import admin
from flask.ext.admin.contrib import peeweemodel
import sqlite3

INVENTORY_STATUS = [(1, 'Checked in'), (2, 'Checked out')]
db = peewee.SqliteDatabase(settings.DATABASE_NAME, check_same_thread=False)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Person(BaseModel):
    name = peewee.CharField(max_length=80, unique=True)

    class Meta:
        ordering = (('name', 'asc'),)

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


class InventoryGroup(BaseModel):
    name = peewee.CharField(max_length=200)

    class Meta:
        ordering = (('name', 'asc'),)

    def __unicode__(self):
        return self.name


class InventoryItem(BaseModel):
    group = peewee.ForeignKeyField(InventoryGroup)
    name = peewee.CharField(max_length=255)
    identifier = peewee.CharField(unique=True, null=True, max_length=500)
    comment = peewee.CharField(null=True, max_length=200)
    date_added = peewee.DateTimeField(null=True)
    date_updated = peewee.DateTimeField()
    status = peewee.IntegerField(default=1, choices=INVENTORY_STATUS)

    class Meta:
        ordering = (('name', 'asc'),)

    def __unicode__(self):
        return self.name

    def get_latest_person(self):
        # get the latest log for this item
        try:
            log = InventoryLog.select().order_by(('date_added', 'DESC')).get(item=self)
        except InventoryLog.DoesNotExist:
            return None
        return log.person


class InventoryLog(BaseModel):
    person = peewee.ForeignKeyField(Person, related_name='logs')
    item = peewee.ForeignKeyField(InventoryItem, related_name='logs')
    status = peewee.IntegerField(default=2, choices=INVENTORY_STATUS)
    date_added = peewee.DateTimeField()

    class Meta:
        ordering = (('date_added', 'desc'),)

    def __unicode__(self):
        return u'%s - %s' % (status, date_added)


def setup():
    tables = (User, InventoryItem, InventoryLog, Person, InventoryGroup)
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
