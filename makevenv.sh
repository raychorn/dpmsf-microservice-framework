#!/bin/bash

if [[ ! -d .venv ]]
then
    virtualenv --python /usr/bin/python3.8 -v .venv
fi

if [[ -d .venv ]]
then
    . ./.venv/bin/activate
    pip install --upgrade pip
    pip install -r microservices-framework/requirements.txt
fi
