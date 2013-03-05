from flask.ext import admin, login, wtf
from flask import url_for, redirect, render_template, request
from models import User
from core import utils


# Define login and registration forms (for flask-login)
class LoginForm(wtf.Form):
    login = wtf.TextField(validators=[wtf.required()])
    password = wtf.PasswordField(validators=[wtf.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise wtf.ValidationError('Invalid user')

        if user.password != self.password.data:
            raise wtf.ValidationError('Invalid password')

    def get_user(self):
        try:
            return User.objects(email=self.login.data).get()
        except User.DoesNotExist:
            pass