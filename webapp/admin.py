from flask.ext import admin, login
from flask import flash
from flask.ext.admin.contrib import peeweemodel as adminview
from models import User, Person, \
    InventoryItem, InventoryLog, InventoryGroup, \
    INVENTORY_STATUS
import sqlite3
from core import app
from core import settings
from core import utils
from core import LONG_DATE_FORMAT, SHORT_DATE_FORMAT, DEFAULT_DATE_FORMAT
from datetime import datetime


def format_status(model, prop_name):
    # format the status field value to a string
    if prop_name == 'status':
        return INVENTORY_STATUS[model.status - 1][1]
    return None


## Base Models
class AdminModelView(adminview.ModelView):
    def is_accessible(self):
        if not login.current_user.is_admin:
            return False
        return login.current_user.is_authenticated()


## Model Admins
class PersonAdmin(AdminModelView):
    searchable_columns = ('name',)


class UserAdmin(AdminModelView):
    list_columns = ('name', 'email')
    searchable_columns = ('email',)


class InventoryItemAdmin(AdminModelView):
    list_columns = ('name', 'identifier', 'status', 'date_updated')
    excluded_form_columns = ('date_added', 'date_updated')
    searchable_columns = ('name', 'identifier')
    list_formatters = {
        'date_updated' : lambda model, p: model.date_updated.strftime(DEFAULT_DATE_FORMAT),
        'status' : format_status
    }

    def create_model(self, form):
        if InventoryItem.filter(identifier=form.identifier.data).exists():
            flash('Identifier (%s) is already in use' % form.identifier.data)
            return False
        # overriden to update the date values of the model
        now = datetime.now()
        item = InventoryItem.insert(
            name=form.name.data,
            identifier=form.identifier.data,
            comment=form.comment.data,
            status=form.status.data,
            group=form.group.data,
            date_added=now,
            date_updated=now
        )
        try:
            item.execute()
        except sqlite3.IntegrityError, e:
            flash('Unable to add the item', category='error')
            if settings.DEBUG:
                flash('%s' % e, category='error')
            return False
        return True

    def update_model(self, form, model):
        model.date_updated = datetime.now()
        return super(AdminModelView, self).update_model(form, model)


class InventoryLogAdmin(AdminModelView):
    can_create = settings.DEBUG
    rename_columns = {'date_added' : 'Date'}
    disallowed_actions = ('delete',) if not settings.DEBUG else []
    list_formatters = {
        'date_added' : lambda model, p: model.date_added.strftime(DEFAULT_DATE_FORMAT),
        'status' : format_status
    }


# Create customized index view class
class AdminIndexView(admin.AdminIndexView):
    @admin.expose('/')
    def index(self):
        html = self.render('admin/index.html',
            user=login.current_user,
            INVENTORY_ITEM_NAME_PLURAL=settings.INVENTORY_ITEM_NAME_PLURAL
        )
        return html

    def is_accessible(self):
        if not login.current_user.is_admin:
            return False
        return login.current_user.is_authenticated()


# Initialize flask-login
def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.select().get(id=user_id)
        except User.DoesNotExist:
            pass


def setup():
    init_login()

    adm = admin.Admin(app, settings.SITE_TITLE+' Admin', index_view=AdminIndexView())

    adm.add_view(UserAdmin(User))
    adm.add_view(PersonAdmin(Person))
    adm.add_view(AdminModelView(InventoryGroup))
    adm.add_view(InventoryItemAdmin(InventoryItem))
    adm.add_view(InventoryLogAdmin(InventoryLog))
    pass