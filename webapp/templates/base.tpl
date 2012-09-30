<!DOCTYPE html>
<html class='{{ html_css_class }}'>

    <head>
        <meta http-equiv="Content-type" content="text/html; charset=utf-8"/>
        <title>{% block title %}{{ title }}{% endblock %} - {{ site_title }}</title>
        <link rel="stylesheet" href="/static/css/bootstrap.min.css">
        <link rel="stylesheet" href="/static/css/bootstrap-responsive.min.css">
        <link rel="stylesheet" href="/static/css/background-gradients.css">
        <link rel="stylesheet" href="/static/css/main.css" type="text/css" charset="utf-8">
        <script src='/static/js/jquery.min.js'></script>
        <script src='/static/js/bootstrap.min.js'></script>

        {% block header %}
        {% endblock %}
    </head>

    <body>
        <div id='top-banner' class="bg-gradient-{{ site_banner_color }} navbar navbar-fixed-top">
            <!-- Start custom banner HTML here -->
            <span id='banner-text'>{{ site_banner_text }}</span>
            <!-- End custom banner HTML here -->

            {% block top_banner %}
            <div id="menu">
                <div class="btn-group">
                  <a class="btn dropdown-toggle" data-toggle="dropdown" href="#">
                    Menu
                    <span class="caret"></span>
                  </a>
                  <ul class="dropdown-menu">
                    {% if user and user.is_authenticated() %}
                    <li><a href="{{ url_for('logout_view') }}">Logout</a></li>
                    <li><a href="{{ url_for('inventory_view') }}">Inventory</a></li>
                    <li><a href="{{ url_for('admin.index') }}">Admin</a></li>
                    {% else %}
                    <li><a href="{{ url_for('login_view') }}">Login</a></li>
                    <li><a href="{{ url_for('inventory_view') }}">Inventory</a></li>
                    {% endif %}
                  </ul>
                </div>
            </div>
            {% endblock %}
        </div>

        <div id="content">
        {% block content %}
            Content here
        {% endblock %}
        </div>
<!--
    For His glory (Hebrews 1, Colossians 1, Genesis 1).
    Copyright 2012 Christopher Bess
-->
    </body>
</html>