#!/bin/sh
python manage.py makemessages -a -v 2
sudo python manage.py compilemessages
:
