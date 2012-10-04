# global
# Created by: Christopher Bess
# It is recomm. not to run this script using sudo, it is used as needed.
#
# Run this script from this `setup` directory.
#
# user$: sh ./virtualenv-setup.sh

VENV_NAME=inventorycheckin_env

# echo "Setting up virtualenv and pip"
sudo easy_install pip
sudo pip install virtualenv

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