"""
Django production settings for spotlight project.
Please only change this for production stage.
"""
from .base import *  # ignore W0614
import os

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ["nft-spotlight.herokuapp.com",
                "spotlight-explorer.herokuapp.com",
                "herokuapp.com",
                "explorer.nft-spotlight.xyz"]
