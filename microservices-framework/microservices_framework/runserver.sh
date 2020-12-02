#!/bin/bash

FILE="./manage.py"
if [[ -f $FILE ]];then
    FILE="manage.py"
else
    FILE="./manage.pyc"
    if [[ -f $FILE ]];then
        FILE="manage.pyc"
    fi
fi

#python $FILE migrate -v 3 --settings microservices_framework.settings --pythonpath "./python_lib3"

python $FILE runserver 0.0.0.0:8088 -v 3 --settings microservices_framework.settings --pythonpath "./python_lib3"
