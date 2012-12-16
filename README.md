inventory-checkin
=================

Inventory check-in/out manager, for a tablet kiosk.

Review the `settings.py` file for configuration details.

## Basic Setup

Instructions:

1. Download [Inventory Checkin](https://github.com/cbess/inventory-checkin) source from [GitHub](https://github.com/cbess/inventory-checkin).
1. Extract/place the source code in the desired (install) directory. This will be where the app lives.
1. Run `sh virtualenv-setup.sh` to setup an isolated environment and download packages.
1. Configure settings. The defaults in `settings.py` provide documentation for each setting.
	- Copy `example.local_settings.py` to `local_settings.py`.
 	- Override/copy any setting from `settings.py` to `local_settings.py` (change the values as needed).
1. Run `source inventorycheckin_env/bin/activate` to enter the virtual environment.
1. Run `python main.py --index update` or `--index rebuild` to index the path specified in the settings. Watch indexing output.
1. Run `python main.py --runserver` to start the web server.
1. Go to `http://localhost:7777` to access the web interface. Uses the [twitter bootstrap](http://twitter.github.com/bootstrap) for its UI.

#### Default Login

    username: admin@example.com
    password: admin

The defaults can be changed in the admin: `http://localhost:7777/admin`.