# -*- coding: utf-8 -*-
# refs: http://flask.pocoo.org/docs/quickstart/#redirects-and-errors

import os
from core import app
from flask import render_template, request, abort, Response, url_for, redirect
from flask.ext import admin, login
from core import settings as core_settings
from core.utils import debug, read_file
from forms import LoginForm
# from template_filters import register_filters

# register template filters
# register_filters(app)


def add_default_response(response):
    """Adds the default response parameters to the response.
    """
    response['site_banner_text'] = core_settings.SITE_BANNER_TEXT
    response['site_title'] = core_settings.SITE_TITLE
    response['site_banner_color'] = core_settings.SITE_BANNER_COLOR
    response["user"] = login.current_user
    pass
    

@app.route('/')
def index():
    """Handles index requests
    """
    response = {
        "title" : u"Welcome"
    }
    add_default_response(response)
    return render_template('index.html', **response)


@app.route('/login/', methods=('GET', 'POST'))
def login_view():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = form.get_user()
        login.login_user(user)
        return redirect(url_for('index'))
    response = {
        'form' : form
    }
    add_default_response(response)
    return render_template('login.html', **response)


@app.route('/logout/')
def logout_view():
    login.logout_user()
    return redirect(url_for('index'))
