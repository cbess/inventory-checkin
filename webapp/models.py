from core import db
from core import settings
from server import app
from flask.ext import admin
import sqlite3

INVENTORY_STATUS = [(1, 'Checked in'), (2, 'Checked out')]


class BaseModel(db.Document):
    pass


class Person(BaseModel):
    name = db.StringField(max_length=80, unique=True)

    def __unicode__(self):
        return self.name


class User(Person):
    email = db.StringField(max_length=120)
    password = db.StringField(max_length=250)
    is_admin = db.BooleanField(default=False)

    class Meta:
        order_by = ('name',)
        
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
    name = db.StringField(max_length=200)

    class Meta:
        order_by = ('name',)

    def __unicode__(self):
        return self.name


class InventoryItem(BaseModel):
    group = db.ReferenceField(InventoryGroup)
    name = db.StringField(max_length=255)
    identifier = db.StringField(unique=True, max_length=500)
    comment = db.StringField(max_length=200)
    date_added = db.DateTimeField()
    date_updated = db.DateTimeField()
    status = db.IntField(default=1, choices=INVENTORY_STATUS)

    class Meta:
        order_by = ('name',)

    def __unicode__(self):
        return self.name

    def get_latest_person(self):
        # get the latest log for this item
        try:
            log = InventoryLog.filter(InventoryLog.item == self).order_by(InventoryItem.date_added.desc()).get()
        except InventoryLog.DoesNotExist:
            return None
        return log.person


class InventoryLog(BaseModel):
    person = db.ReferenceField(Person)
    item = db.ReferenceField(InventoryItem)
    status = db.IntField(default=2, choices=INVENTORY_STATUS)
    date_added = db.DateTimeField()

    class Meta:
        order_by = ('-date_added',)

    def __unicode__(self):
        return u'%s - %s' % (status, date_added)


def setup():
    tables = (User, InventoryItem, InventoryLog, Person, InventoryGroup)
    for table in tables:
        try:
            # table.create_table()
            if User == table:
                # add an admin user
                User(
                    name='admin',
                    email='admin@example.com',
                    password='admin',
                    is_admin=True
                ).save()
                pass
        except sqlite3.OperationalError:
            # table may already exist
            pass
