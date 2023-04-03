"""
Django production settings for spotlight project.
Please only change this for production stage.
"""
from .base import *  # ignore W0614
import os

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ["*"]
