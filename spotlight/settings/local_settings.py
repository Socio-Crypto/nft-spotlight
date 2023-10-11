"""
Django local settings for spotlight project.
Write your local settings here, other global settings is imported from base.py
"""
from .base import *  # ignore W0614
import os
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'spotlight'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', '1234'),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.manage.py.django.DjangoTemplates',
#         'DIRS': [
#             BASE_DIR / "templates",
#             BASE_DIR / "frontend/build",
            
#         ],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]
