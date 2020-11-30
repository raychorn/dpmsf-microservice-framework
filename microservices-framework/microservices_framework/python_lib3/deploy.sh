#!/bin/bash

python -m compileall -f
find . -type f | grep -e "*.py" | xargs rm -rf