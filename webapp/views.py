# -*- coding: utf-8 -*-
# refs: http://flask.pocoo.org/docs/quickstart/#redirects-and-errors

import os
from core import app, cache
from flask import render_template, request, abort, Response, url_for, redirect
from flask.ext import admin, login
from core import settings as core_settings
from core.utils import debug, read_file
from forms import LoginForm
from models import Person, InventoryLog, InventoryItem, \
     InventoryGroup, CheckoutMeta, DURATION_TYPES
from datetime import datetime
import json
import re
# from template_filters import register_filters

# register template filters
# register_filters(app)

# regex to get a sort number from the item name and sort the items
sort_items_regex = None
if core_settings.INVENTORY_ITEM_NAME_SORT_NUMBER_REGEX:
    sort_items_regex = re.compile(core_settings.INVENTORY_ITEM_NAME_SORT_NUMBER_REGEX)


def add_default_response(response):
    """Adds the default response parameters to the response.
    """
    response['user'] = login.current_user
    response['site_banner_text'] = core_settings.SITE_BANNER_TEXT
    response['site_title'] = core_settings.SITE_TITLE
    response['site_banner_color'] = core_settings.SITE_BANNER_COLOR
    response['INVENTORY_ITEM_NAME'] = core_settings.INVENTORY_ITEM_NAME
    response['INVENTORY_ITEM_NAME_PLURAL'] = core_settings.INVENTORY_ITEM_NAME_PLURAL
    # simple mobile (iphone/ipad) check
    response['is_mobile'] = (request.headers.get('User-Agent', '').find('Mobile') >= 0)
    

def get_sorted_inventory_items(items):
    """Sorts the specified InventoryItem objects"""
    if not sort_items_regex:
        return items
    def sort_key(item):
        """Returns the key that should be sorted"""
        try:
            return int(sort_items_regex.search(item.name).group(1))
        except (ValueError, AttributeError), e:
            if not core_settings.DEBUG:
                # return default
                return ''
            # re-raise with more information
            raise Exception(
                'Unable to get an item sort number regex group, check the '
                'INVENTORY_ITEM_NAME_SORT_NUMBER_REGEX setting: %s = %s' %
                (core_settings.INVENTORY_ITEM_NAME_SORT_NUMBER_REGEX, item.name))
    return sorted(items, key=sort_key)

    
@app.route('/favicon.ico', methods=('GET',))
def favicon():
    return app.send_static_file('favicon.ico')


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
        if not user.is_admin:
            return redirect(url_for('inventory_view'))
        else:
            return redirect(url_for('admin.index'))
    response = {
        'form' : form
    }
    add_default_response(response)
    return render_template('login.html', **response)


@app.route('/logout/')
def logout_view():
    login.logout_user()
    return redirect(url_for('index'))


@app.route('/inventory/')
@cache.cached()
def inventory_view():
    items = InventoryItem.objects
    group_id = request.args.get('group')
    if group_id:
        group = InventoryGroup.objects.get(identifier=group_id)
        items = items(group=group)
    # build response
    response = {
        'items' : get_sorted_inventory_items(items),
        'persons' : Person.objects.all(),
        'groups' : InventoryGroup.objects.all(),
        'duration_types' : DURATION_TYPES[1:],
        'group_id' : group_id if group_id else '',
        'title' : core_settings.INVENTORY_ITEM_NAME_PLURAL,
        'confirmation' : core_settings.USER_CONFIRMATION,
        'inventory_auto_refresh' : core_settings.INVENTORY_AUTO_REFRESH
    }
    add_default_response(response)
    return render_template('inventory.html', **response)
# the cache key should be composed of path and query params
inventory_view.make_cache_key = lambda *args, **kwargs: request.path+request.query_string+unicode(login.current_user)


# ajax only
@app.route('/inventory/update', methods=['POST'])
def inventory_update_view():
    if login.current_user.is_anonymous():
        abort()
    # 1 = checkin, 2 = checkout
    status = int(request.form['status'])
    checkout_meta = None
    # provide meta
    if status == 2: # checkout
        dtype = int(request.form['duration_type'])
        duration = request.form['duration']
        try:
            duration = int(duration)
        except ValueError:
            duration = 0
        checkout_meta = CheckoutMeta(
            duration=duration,
            duration_type=dtype,
            is_ooo=(True if int(request.form.get('ooo', 0)) else False)
        )
    # add a log
    log = InventoryLog(
        person=Person.objects(id=request.form['personid']).get(),
        item=InventoryItem.objects(id=request.form['itemid']).get(),
        status=int(request.form['status']),
        date_added=datetime.now(),
        checkout_meta=checkout_meta
    )
    log.save()
    # update the item status
    item = InventoryItem.objects(id=request.form['itemid']).get()
    item.status = status
    item.save()
    response = {
        'duration': {
            'dateAdded' : log.get_date_added(),
            'description': log.get_checkout_description()
        },
        'person': {
            'name' : log.person.name
        }
    }
    return json.dumps(response)
    
    