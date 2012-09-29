from flask.ext import admin, login
from flask.ext.admin.contrib import peeweemodel as adminview
from models import User
from core import app
from core import settings
from core import utils

class AdminModelView(adminview.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated()


class UserAdmin(AdminModelView):
    list_columns = ('username', 'email')
    searchable_columns = ('username', User.username)


# Create customized index view class
class AdminIndexView(admin.AdminIndexView):
    @admin.expose('/')
    def index(self):
        return self.render('admin/index.html', user=login.current_user)

    def is_accessible(self):
        return login.current_user.is_authenticated()


# Initialize flask-login
def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.select().get(id=user_id)


def setup():
    init_login()

    adm = admin.Admin(app, settings.SITE_TITLE+' Admin', index_view=AdminIndexView())

    adm.add_view(UserAdmin(User))
    pass