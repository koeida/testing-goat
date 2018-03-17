#! /bin/sh

find . -maxdepth 2 -name '*.py' | entr sh -c 'python manage.py test'
