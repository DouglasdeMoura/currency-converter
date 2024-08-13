#!/bin/sh

PYTHONPATH=/code
python manage.py migrate
daphne -b 0.0.0.0 -p 8000 currency_converter.asgi:application
