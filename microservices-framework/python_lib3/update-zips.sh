#!/bin/bash

zip_file=python_lib3.zip
wget -O ./$zip_file  https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2Fraychorn%2Fmicroservices-fram>

if [[ -f $zip_file ]]
then
    echo "Found $zip_file"
fi
