#!/bin/bash

wget -O ./python_lib3  https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2Fraychorn%2Fmicroservices-framework%2Ftree%2Fmain%2Fmicroservices-framework%2Fpython_lib3

zip_file=$(ls *.zip)
if [[ -f $zip_file ]]
then
    echo "Found $zip_file"
fi
