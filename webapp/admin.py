from flask.ext import admin, login
from flask import flash
from flask.ext.admin.contrib import mongoengine as adminview
from mongoengine.queryset import Q
from models import User, Person, \
    InventoryItem, InventoryLog, InventoryGroup, \
    INVENTORY_STATUS
import sqlite3
from core import app
from core import settings
from core import utils
from core import LONG_DATE_FORMAT, SHORT_DATE_FORMAT, DEFAULT_DATE_FORMAT
from datetime import datetime
import forms


def format_prop(context, model, prop_name):
    # format the status field value to a string
    if prop_name == 'status':
        return INVENTORY_STATUS[model.status - 1][1]
    elif prop_name == 'group':
        try:
            return model.group.name
        except InventoryGroup.DoesNotExist:
            return 'None'
    return None
    
    
def can_access_admin(user):
    # determines if the specified user can access the admin
    if user.is_anonymous():
        return False
    if not user.is_authenticated() or not user.is_admin:
        return False
    return user.is_authenticated()


## Base Models
class AdminModelView(adminview.ModelView):
    def is_accessible(self):
        user = login.current_user
        return can_access_admin(user)

## Model Admins
class PersonAdmin(AdminModelView):
    column_searchable_list = ('name',)


class UserAdmin(AdminModelView):
    column_list = ('name', 'email')
    column_searchable_list = ('email',)


class InventoryItemAdmin(AdminModelView):
    form = forms.InventoryItemForm
    column_list = ('name', 'identifier', 'status', 'group', 'date_updated')
    form_excluded_columns = ('date_added', 'date_updated')
    column_searchable_list = ('name', 'identifier')
    column_formatters = {
        'date_updated' : lambda ctx, model, prop: model.date_updated.strftime(DEFAULT_DATE_FORMAT),
        'status' : format_prop,
        'group' : format_prop
    }    
        
    def create_model(self, form):
        # only if its set do we care if its unique
        if form.identifier.data and InventoryItem.objects(identifier=form.identifier.data).count():
            flash('Identifier (%s) is already in use' % form.identifier.data)
            return False
        # overriden to update the date values of the model
        now = datetime.now()
        item = InventoryItem(
            name=form.name.data,
            identifier=form.identifier.data,
            comment=form.comment.data,
            status=form.status.data,
            # get the model for the target group
            group=InventoryGroup.objects.get(id=form.group.data),
            date_added=now,
            date_updated=now
        )
        try:
            item.save()
        except Exception, e:
            flash('Unable to add the item', category='error')
            if settings.DEBUG:
                flash('DEBUG: %s' % e, category='error')
            return False
        return True

    def update_model(self, form, model):
        model.date_updated = datetime.now()
        # super will save it for us, change it to a model ref
        form.group.data = InventoryGroup.objects.get(id=form.group.data)
        return super(AdminModelView, self).update_model(form, model)


class InventoryLogAdmin(AdminModelView):
    can_create = settings.DEBUG
    column_labels = {'date_added' : 'Date'}
    action_disallowed_list = ('delete',) if not settings.DEBUG else []
    column_formatters = {
        'date_added' : lambda ctx, model, prop: model.date_added.strftime(DEFAULT_DATE_FORMAT),
        'status' : format_prop
    }
    form_args = {'status': {'coerce': int}}

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
        return can_access_admin(login.current_user)


# Initialize flask-login
def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.objects(id=user_id).get()
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
