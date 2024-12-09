import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_algebra_calculator.settings')

application = get_wsgi_application()

app = application