#!/bin/bash

CURDIR=$(python -c "import os; print(os.path.dirname(os.path.abspath(os.curdir)))")
echo "CURDIR -> $CURDIR"

RUNSERVER=$(find $CURDIR -name runserver.sh | grep runserver.sh)
echo "RUNSERVER -> $RUNSERVER"

nohup $RUNSERVER > server.log 2>&1 &

TESTS=$(find $CURDIR -name test_restful.py | grep test_restful.py)
echo "TESTS -> $TESTS"

echo "Sleeping for 10 seconds…"
sleep 10
echo "Completed"

pytest $TESTS -v

INFO=$(ps -aux | grep /microservices_framework/manage.py)
echo "INFO -> $INFO"

set -- $INFO
echo "pid -> $2"
kill -9 $2
