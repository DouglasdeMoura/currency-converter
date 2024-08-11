import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "currency_converter.settings")

django.setup()
