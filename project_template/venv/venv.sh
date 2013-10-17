#!/bin/bash

set -e  # If occur any error, exit
set -x  # Verbose mode

function to_console {
    echo -e "\n*** $1 ***\n"
}

to_console "Setting up virtualenv on venv"

source bin/activate || (cd .. && virtualenv -p /usr/bin/python2.7 venv && cd venv && source bin/activate)

to_console "Checking up dependencies"

pip install -r dev_requirements.txt --upgrade --use-mirrors


cd ../src

if [ ! -d lib ]; then
    to_console "Creating symlink on src/lib so installed libs become visible to Google App Engine"
    ln -s ../venv/lib/python2.7/site-packages lib
fi





