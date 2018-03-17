#! /bin/sh

ag -l | entr sh -c 'python manage.py test'
