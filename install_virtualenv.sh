#!/bin/sh
#
# Hope You will find it usefull :)

wget --no-check-certificate https://raw.github.com/pypa/virtualenv/1.9.X/virtualenv.py 
python virtualenv.py flask
while read line; do flask/bin/pip install $line; done < requirements.txt
