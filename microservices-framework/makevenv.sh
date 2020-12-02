#!/bin/bash

if [[ ! -d .venv ]]
then
    virtualenv --python /usr/local/bin/python3.8 -v .venv
fi

. ./.venv/bin/activate
pip install --upgrade pip
pip install -r ./requirements.txt
