#!/bin/bash

LIB_SRC=/workspaces/private-microservices-framework/microservices_framework/python_lib3/private_vyperlogix_lib3/zips
FRAMEWORK_SRC=/workspaces/private-microservices-framework/microservices_framework
LIB_DEST=/workspaces/microservices-framework/microservices-framework/python_lib3
FRAMEWORK_DEST=/workspaces/microservices-framework/microservices-framework

if [[ -d $FRAMEWORK_SRC ]]
then
    echo "Updating FRAMEWORK"
    mv $FRAMEWORK_DEST/.env $FRAMEWORK_DEST/..
    rm -R -f $FRAMEWORK_DEST/
    mkdir -p $FRAMEWORK_DEST
    cp -R -f $FRAMEWORK_SRC/* $FRAMEWORK_DEST
    rm -R -f $FRAMEWORK_DEST/python_lib3/*
    find $FRAMEWORK_DEST -name __pycache__ -exec rm -rf {} \;
    mv $FRAMEWORK_DEST/../.env $FRAMEWORK_DEST
fi

if [[ -d $LIB_SRC ]]
then
    echo "Updating ZIPS"
    rm -f $LIB_DEST/*.zip
    cp $LIB_SRC/*.zip $LIB_DEST
fi

