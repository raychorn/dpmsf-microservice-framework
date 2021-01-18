#!/bin/bash

VENV=.venv
REQS=requirements.txt

git pull origin main

dir="./microservices-framework"

python=/usr/bin/python3.8
vers=$($python -c 'import sys; i=sys.version_info; print("{}{}{}".format(i.major,i.minor,i.micro))')

if [[ ! -d $VENV$vers ]]
then
    virtualenv --python $python -v $VENV$vers
fi

. $VENV$vers/bin/activate
pip install -r $dir/$REQS

gunicorn -c $dir/config.py microservices_framework.wsgi:application
