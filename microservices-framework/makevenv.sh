#!/bin/bash

virtualenv --python /usr/local/bin/python3.8 -v .venv

. ./.venv/bin/activate
pip install --upgrade pip
pip install -r ./requirements.txt
