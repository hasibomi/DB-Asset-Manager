"""
WSGI config for project_db_asset_manager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/var/www/html/db-asset-manager.cimplux.com')
# adjust the Python version in the line below as needed
sys.path.append('/var/www/html/db-asset-manager.cimplux.com/env/lib/python3.6/site-packages')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_db_asset_manager.settings')

application = get_wsgi_application()
