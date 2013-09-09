<!DOCTYPE html>
{% if current_user %}
{% set can_edit = current_user.is_authenticated() %}
{% endif %}
<html class='{{ html_css_class }}{% if is_mobile %} mobile{% endif %}{% if can_edit %} edit{% endif %}'>

    <head>
        <meta http-equiv="Content-type" content="text/html; charset=utf-8"/>
        <meta name="google" value="notranslate"/>
        <title>{% block title %}{{ title }}{% endblock %} - {{ site_title }}</title>
        <link rel="stylesheet" href="/static/css/bootstrap.min.css">
        <link rel="stylesheet" href="/static/css/bootstrap-responsive.min.css">
        <link rel="stylesheet" href="/static/css/background-gradients.css">
        <link rel="stylesheet" href="/static/css/main.css" type="text/css" charset="utf-8">
        <script src='/static/js/jquery.min.js'></script>
        <script src='/static/js/jquery.string.min.js'></script>
        <script src='/static/js/bootstrap.min.js'></script>
        <script src='/static/js/toastr.min.js'></script>

        {% block header %}
        {% endblock %}
    </head>

    <body>
        <div id="top-banner" class="navbar navbar-fixed-top">
            <div class="navbar-inner {% if site_banner_color %}bg-gradient-{{ site_banner_color }}{% endif %}">
                <div class="container">
                    <!-- Start custom banner HTML here -->
                    <span id='banner-text'><a class="brand" href="javascript:void(0)">{{ site_banner_text }}</a></span>
                    <!-- End custom banner HTML here -->

                    {% block top_banner %}
                    <div id="menu">
                        <div class="btn-group">
                          <a class="btn dropdown-toggle" data-toggle="dropdown" href="#">
                            Menu
                            <span class="caret"></span>
                          </a>
                          <ul class="dropdown-menu">
                            {% if can_edit %}
                            <li><a href="{{ url_for('logout_view') }}">Logout</a></li>
                            <li><a href="{{ url_for('inventory_view') }}">{{ INVENTORY_ITEM_NAME_PLURAL }}</a></li>
                            {% if current_user.is_admin %}
                            <li><a href="{{ url_for('admin.index') }}">Admin</a></li>
                            {% endif %}
                            {% else %}
                            <li><a href="{{ url_for('login_view') }}">Login</a></li>
                            <li><a href="{{ url_for('inventory_view') }}">{{ INVENTORY_ITEM_NAME_PLURAL }}</a></li>
                            {% endif %}
                          </ul>
                        </div>
                    </div>
                    {% endblock %}
                </div>
            </div>
        </div>

        <div id="content">
        {% block content %}
            Content here
        {% endblock %}
        </div>
<!--
    For His glory (Hebrews 1, Colossians 1, Genesis 1).
    Copyright 2013 Christopher Bess
-->
    </body>
</html>