#!/bin/bash

#python manage.pyc migrate -v 3 --settings microservices_framework.settings --pythonpath "./python_lib3"

python manage.pyc runserver 0.0.0.0:8088 -v 3 --settings microservices_framework.settings --pythonpath "./python_lib3"
