from core import peewee
from flask.ext import admin
from flask.ext.admin.contrib import peeweemodel

db = peewee.SqliteDatabase('webapp.db', check_same_thread=False)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class User(BaseModel):
    username = peewee.CharField(max_length=80)
    password = peewee.CharField(max_length=250)
    email = peewee.CharField(max_length=120)

    def __unicode__(self):
        return self.username


def setup():
    try:
        User.create_table()
    except:
        pass
