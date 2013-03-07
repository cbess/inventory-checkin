inventory-checkin
=================

Inventory check-in/out manager, for a tablet kiosk.

Review the `settings.py` file for configuration details.

Note: This is **beta** software.

![ICI Kiosk Image](https://github.com/cbess/inventory-checkin/raw/master/ici-screenshot.jpeg)
**Kiosk**

![ICI Admin Image](https://github.com/cbess/inventory-checkin/raw/master/ici-admin.jpg)
**Admin**

## Basic Setup

**Requires**
    
- [Python](http://python.org) +2.6
- [MonogoDB](http://www.mongodb.org) +2.x

Instructions:

1. Download [Inventory Checkin](https://github.com/cbess/inventory-checkin) source from [GitHub](https://github.com/cbess/inventory-checkin).
1. Extract/place the source code in the desired (install) directory. This will be where the app lives.
1. Run `sh virtualenv-setup.sh` to setup an isolated environment and download dependencies.
1. Configure settings. The defaults in `settings.py` provide documentation for each setting.
	- Copy `settings.py` to `local_settings.py`.
 	- Override/copy any setting from `settings.py` to `local_settings.py` (change the values as needed).
1. Run `source inventorycheckin_env/bin/activate` to enter the virtual environment.
1. Run `python main.py --index update` or `--index rebuild` to index the path specified in the settings. Watch indexing output.
1. Run `python main.py --runserver` to start the web server.
1. Go to `http://localhost:7777` to access the web interface. Uses the [twitter bootstrap](http://twitter.github.com/bootstrap) for its UI.

#### Default Login

    username: admin@example.com
    password: admin

The defaults can be changed in the admin: `http://localhost:7777/admin`.

### Usage Scenario

This web app will allow you to setup users which are either, admin or only authenticated. However, the system works with three user types: `admin`, `authenticated`, and `anonymous`.

Typical scenario (setup):

CO/I = Check Out and In

1. Login as the admin.
1. Update the admin user credentials (if needed).
1. Import/create persons that can co/i inventory items.
1. Add groups and inventory items to the groups.
1. Create an authenticated (non-admin) user for the kiosks/tablets. This will allow the user to co/i inventory items, but no access is given to the admin panel.
1. Login using the kiosk credentials on the desired device.
    - Go to `/inventory`.
    - All other users can then co/i items from that device.
1. Anonymous users can now view the co/i status of the items in the inventory.
    - Go to `/inventory`.
    - It is a readonly view of the inventory, that auto-refreshes.

### Deployment Notes

Sample `supervisord.conf` section:

	[program:inventorymate]
	command = /path/to/inventorymate/inventorycheckin_env/bin/python main.py --runserver
	directory = /path/to/inventorymate
	stdout_logfile = /path/to/inventorymate.log
