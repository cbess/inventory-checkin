# global
# https://github.com/cbess/inventory-checkin - Christopher Bess - Copyright 2014
# It is recomm. not to run this script using sudo, it is used as needed.
#
# Run this script from this `setup` directory.
#
# user$: sh ./virtualenv-setup.sh

VENV_NAME=inventorycheckin_env

# If `DistributionNotFound` error is shown then try running:
# Download ez_setup.py - http://peak.telecommunity.com/dist/ez_setup.py
# sudo python ez_setup.py -U setuptools

# echo "Setting up virtualenv and pip"
if command -v pip > /dev/null 2>&1 ; then
    echo 'pip already installed'
else
    sudo easy_install pip
fi

if command -v virtualenv > /dev/null 2>&1 ; then
    echo 'virtualenv already installed'
else
    sudo pip install virtualenv
fi

# adjust permission (allow it to be executed)
chmod +x ../main.py

# if on a Mac exec below line (maybe)
# ARCHFLAGS="-arch i386 -arch x86_64"

# setup sherlock environment
virtualenv ../$VENV_NAME --distribute --no-site-packages

echo "Installing dependencies"
../$VENV_NAME/bin/pip install -r requirements.txt

# confirm installation by showing version information
# echo "Sherlock version information"
# ../$VENV_NAME/bin/python ../main.py -v

echo "Done, install finished"
