#!/bin/bash

ISPUBLIC=$(pwd | grep public)
ISPRIVATE=$(pwd | grep private)

DIR="/workspaces/private-microservices-framework/microservices_framework"
if [[ $ISPUBLIC. == . ]];then
    echo "Not PUBLIC"
    DIR="/workspaces/private-microservices-framework/microservices_framework"
fi

if [[ $ISPRIVATE. == . ]];then
    echo "Not PRIVATE"
    DIR="/workspaces/public-microservices-framework/microservices_framework"
fi

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

LIB=$(find $CURDIR -name python_lib3 | grep python_lib3)
echo "LIB -> $LIB"
if [[ $LIB. == . ]];then
    echo "Not found python_lib3"
    exit
fi

#python $FILE migrate -v 3 --settings microservices_framework.settings --pythonpath "./python_lib3"

python $MANAGEPY runserver 127.0.0.1:8088 -v 3 --settings microservices_framework.settings --pythonpath "$LIB"
