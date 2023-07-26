import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE","LightweightBugManagementPlatform.settings")
django.setup()

from web import models
models.UserInfo.objects.create(username='script1', email='p@g.com',mobile_phone='+16696696696',password='123')