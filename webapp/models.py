from core import db
from core import settings
from core import utils
from server import app
from flask.ext import admin
import mongoengine
import datetime

INVENTORY_STATUS = [(1, 'Checked in'), (2, 'Checked out')]
# CheckoutMeta duration type, if changed here then 
# change CheckoutMeta.DURATION_TYPE_* values
DURATION_TYPES = [(0, 'Soon'), (1, 'Minutes'), (2, 'Hours'), (3, 'Days')]


class Person(db.Document):
    name = db.StringField(max_length=80, unique=True)
    meta = {'ordering': ['name']}
        
    def __unicode__(self):
        return self.name
        
        
class User(db.Document):
    name = db.StringField(max_length=80, unique=True)
    email = db.StringField(max_length=120)
    password = db.StringField(max_length=250)
    is_admin = db.BooleanField(default=False)
    meta = {'ordering': ['name']}
    
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
    identifier = db.StringField(unique=True, max_length=33)
    meta = {'ordering': ['name']}

    def __unicode__(self):
        return self.name


class InventoryItem(db.Document):
    group = db.ReferenceField(InventoryGroup, dbref=True)
    name = db.StringField(max_length=255)
    identifier = db.StringField(max_length=500)
    comment = db.StringField(max_length=200)
    date_added = db.DateTimeField()
    date_updated = db.DateTimeField()
    status = db.IntField(default=1, choices=INVENTORY_STATUS)
    meta = {'ordering': ['name']}

    def __unicode__(self):
        return self.name

    def get_latest_log(self):
        """Return the latest log for this item"""
        try:
            log = InventoryLog.objects(item=self).order_by('-date_added').first()
            if not log:
                return None
        except InventoryLog.DoesNotExist:
            return None
        return log    
    
    def get_latest_person(self):
        """Return the latest person for this item"""
        log = self.get_latest_log()
        if not log:
            return None
        return log.person


class CheckoutMeta(db.EmbeddedDocument):
    # constants
    DURATION_TYPE_UNKNOWN = 0
    DURATION_TYPE_MINS = 1
    DURATION_TYPE_HOURS = 2
    DURATION_TYPE_DAYS = 3
    # fields
    duration = db.FloatField(default=0)
    duration_type = db.IntField(default=DURATION_TYPE_UNKNOWN, choices=DURATION_TYPES)
    is_ooo = db.BooleanField(default=False) # out of office


class InventoryLog(db.Document):
    person = db.ReferenceField(Person, dbref=True)
    item = db.ReferenceField(InventoryItem, dbref=True)
    status = db.IntField(default=2, choices=INVENTORY_STATUS)
    date_added = db.DateTimeField(default=datetime.datetime.now)
    checkout_meta = db.EmbeddedDocumentField(CheckoutMeta)
    meta = {'ordering': ['-date_added']}

    def __unicode__(self):
        return u'%s - %s' % (self.status, self.date_added)
        
    def get_checkout_description(self):
        """Returns a human-readable description for the checkout"""
        name = u''
        if not self.checkout_meta:
            return name
        # no duration, then assume default
        duration = self.checkout_meta.duration
        if not duration:
            return u'soon'
        # determine name of duration
        dtype = self.checkout_meta.duration_type
        if dtype == CheckoutMeta.DURATION_TYPE_UNKNOWN:
            return u'soon'
        elif dtype == CheckoutMeta.DURATION_TYPE_MINS:
            name = u'min'
        elif dtype == CheckoutMeta.DURATION_TYPE_HOURS:
            name = u'hr'
        elif dtype == CheckoutMeta.DURATION_TYPE_DAYS:
            name = u'day'
        # format OOO
        ooo_str = ''
        if self.checkout_meta.is_ooo:
            ooo_str = ' OOO'
        # pluralize name
        if duration > 1: 
            name += u's'
        description = u'{duration:.0f} {dname}{ooo}'.format(
            duration=duration, 
            dname=name, 
            ooo=ooo_str
        )
        return description
        
    def get_date_added(self):
        """Returns a formatted date added value"""
        # ref: http://docs.python.org/2/library/time.html#time.strftime
        return self.date_added.strftime(settings.INVENTORY_CHECKOUT_DATE_FORMAT)


def setup():
    tables = (User, InventoryItem, InventoryLog, Person, InventoryGroup)
    # setup defaults for each document, if needed
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
