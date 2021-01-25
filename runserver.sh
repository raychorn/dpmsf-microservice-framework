# deploy this into /workspaces in the container

do_it(){
    REQS=requirements.txt

    dir1="/workspaces/microservices-framework/"
    dir2="$dir1/microservices-framework"
    VENV=$dir1/.venv

    cd $dir1
    #git pull origin main

    python=/usr/bin/python3.8
    vers=$($python -c 'import sys; i=sys.version_info; print("{}{}{}".format(i.major,i.minor,i.micro))')

    if [[ ! -d $VENV$vers ]]
    then
        virtualenv --python $python -v $VENV$vers
    fi

    vyperlib=$dir2/python_lib3/vyperlogix38.zip
    if [[ ! -f $vyperlib ]]
    then
        echo "Cannot find $vyperlib"
        exit
    fi

    . $VENV$vers/bin/activate
    pip install -r $dir2/$REQS

    cd $dir2
    export PYTHONPATH=/workspaces:$dir2:$vyperlib
    #ls -la
    #python -m debug1
    python $MANAGEPY migrate -v 3 --settings microservices_framework.settings
    #python ./manage.py runserver 10.5.0.6:9000 -v 3 --settings microservices_framework.settings
    gunicorn -c $dir2/config.py --workers 4 --max-requests 1 microservices_framework.wsgi:application
}

do_it >/var/log/django/runserver_report.txt 2>&1
