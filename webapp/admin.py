from flask.ext import admin
from flask.ext.admin.contrib import peeweemodel as adminview
from models import User
from core import app


class UserAdmin(adminview.ModelView):
    list_columns = ('username', 'email')
    searchable_columns = ('username', User.username)


def setup():
    adm = admin.Admin(app, 'Webapp Models')

    adm.add_view(UserAdmin(User))
    pass