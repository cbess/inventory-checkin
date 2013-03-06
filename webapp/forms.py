from flask.ext import admin, login, wtf
from flask import url_for, redirect, render_template, request
from models import User, INVENTORY_STATUS, InventoryGroup
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
            
            
class InventoryItemForm(wtf.Form):
    """Represents the admin inventory item form"""
    group = wtf.SelectField()
    name = wtf.TextField(validators=[wtf.required()])
    identifier = wtf.TextField()
    status = wtf.SelectField(choices=INVENTORY_STATUS, coerce=int)
    comment = wtf.TextAreaField()
    
    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        super(InventoryItemForm, self).__init__(request.form, obj, prefix, **kwargs)
        self.csrf_enabled = False
        self.group.choices = [(grp.id, grp.name) for grp in InventoryGroup.objects]
        
    def validate(self, extra_validators=None):
        success = True
        # utils.debug()
        # run validation for fields
        for field in (self.name, self.status):
            if not field.validate(self.data):
                success = False
                self.errors[field.name] = field.errors
        return success
        
    def process(self, formdata=None, obj=None, **kwargs):
        super(InventoryItemForm, self).process(formdata, obj, **kwargs)
        if self.is_submitted():
            # convert to admin model friendly types
            self.group.data = InventoryGroup.objects.get(id=self.group.data)
            self.status.data = int(self.status.data)
        