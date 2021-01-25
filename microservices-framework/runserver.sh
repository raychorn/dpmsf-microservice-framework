#!/bin/bash

export PYTHONPATH=/workspaces/private-microservices-framework/microservices_framework:/workspaces/private_vyperlogix_lib3

ISPUBLIC=$(pwd | grep public)
ISPRIVATE=$(pwd | grep private)

DIR="/workspaces/private-microservices-framework/microservices_framework"
if [[ $ISPUBLIC. == . ]];then
    echo "Private Version"
    DIR="/workspaces/private-microservices-framework/microservices_framework"
fi

if [[ $ISPRIVATE. == . ]];then
    echo "Public Version"
    DIR="/workspaces/public-microservices-framework/microservices_framework"
fi

py=$(ls ../.venv*/bin/activate)
echo "Using $py"
. $py

CURDIR=$(python -c "import os; print(os.path.dirname(os.path.abspath(os.curdir)))")
echo "CURDIR -> $CURDIR"

MANAGEPY=$(find $CURDIR -name manage.py | grep manage.py)
echo "MANAGEPY -> $MANAGEPY"
if [[ $MANAGEPY. == . ]];then
    echo "Not found manage.py"
    MANAGEPY=$(find $CURDIR -name manage.pyc | grep manage.pyc)
    echo "MANAGEPY -> $MANAGEPY"
    if [[ $MANAGEPY. == . ]];then
        echo "Not found manage.pyc"
        exit
    fi
fi

echo "Running migrations..."
python $MANAGEPY migrate -v 3 --settings microservices_framework.settings

dev_server_choice="dev-server"
gunicorn_choice="gunicorn"
uwsgi_choice="uwsgi"
ARRAY=()
ARRAY+=($dev_server_choice)
ARRAY+=($gunicorn_choice)
ARRAY+=($uwsgi_choice)

PS3="Choose: "

select option in "${ARRAY[@]}";
do
    echo "???: $REPLY"
    choice=${ARRAY[$REPLY-1]}
    break
done

echo "Use this -> $choice"

if [[ $choice. == $dev_server_choice. ]];then
    echo "Running $dev_server_choice"
    python $MANAGEPY runserver 127.0.0.1:9000 --settings microservices_framework.settings
fi

if [[ $choice. == $gunicorn_choice. ]];then
    echo "Running $gunicorn_choice"
    env=$(ls -a .. | grep \\.venv)
    echo "Using $env"
    pyv=$(ls ../.venv*/lib)
    echo "Using $pyv"
    gunicorn -c ./config.py microservices_framework.wsgi:application
    #gunicorn -b 127.0.0.1:9000 -w 1 --reload True --pythonpath "./microservices_framework,./python_lib3,./python_lib3/private_vyperlogix_lib3,../$env/lib/$pyv/site-packages" --env DJANGO_SETTINGS_MODULE=microservices_framework.settings microservices_framework.wsgi
fi

if [[ $choice. == $uwsgi_choice. ]];then
    echo "Running $uwsgi_choice"

    if [ ! -d /usr/local/var ];then
        mkdir /usr/local/var
    fi

    if [ ! -d /usr/local/var/log ];then
        mkdir /usr/local/var/log
    fi

    if [ ! -d /usr/local/var/log/uwsgi ];then
        mkdir /usr/local/var/log/uwsgi
    fi

    if [ ! -f /usr/local/var/log/uwsgi/django-wsgi.log ];then
        touch /usr/local/var/log/uwsgi/django-wsgi.log
    fi

    if [ ! -d /usr/local/var/run ];then
        mkdir /usr/local/var/run
    fi

    if [ ! -d /usr/local/var/run/uwsgi ];then
        mkdir /usr/local/var/run/uwsgi
    fi

    uwsgi ./django-wsgi.ini
fi
