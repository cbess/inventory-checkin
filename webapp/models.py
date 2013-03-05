from core import db
from core import settings
from server import app
from flask.ext import admin
import mongoengine

INVENTORY_STATUS = [(1, 'Checked in'), (2, 'Checked out')]


class Person(db.Document):
    name = db.StringField(max_length=80, unique=True)
        
    class Meta:
        order_by = ('name',)
        
    def __unicode__(self):
        return self.name
        
        
class User(db.Document):
    name = db.StringField(max_length=80, unique=True)
    email = db.EmailField(max_length=120)
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


class InventoryGroup(db.Document):
    name = db.StringField(max_length=200)

    class Meta:
        order_by = ('name',)

    def __unicode__(self):
        return self.name


class InventoryItem(db.Document):
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
            log = InventoryLog.objects(item=self).order_by(InventoryItem.date_added.desc()).get()
        except InventoryLog.DoesNotExist:
            return None
        return log.person


class InventoryLog(db.Document):
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
            if User == table:
                # add an admin user
                User(
                    name='admin',
                    email='admin@example.com',
                    password='admin',
                    is_admin=True
                ).save()
        except mongoengine.document.NotUniqueError:
            # already exists
            pass
