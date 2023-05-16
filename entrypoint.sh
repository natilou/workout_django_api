#!/bin/sh
python workout/manage.py makemigrations --settings=workout.settings
python workout/manage.py migrate --settings=workout.settings
python workout/manage.py runserver 0.0.0.0:8000 --settings=workout.settings