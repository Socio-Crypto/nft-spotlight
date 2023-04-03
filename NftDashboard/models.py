from configparser import MAX_INTERPOLATION_DEPTH
from email.policy import default
from enum import unique
from django.db import models


class Collection(models.Model):
    name = models.CharField(blank=True, null=True, max_length=100)
    image = models.ImageField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    collection_name = models.CharField(blank=True, null=True, max_length=100)
    blockchain = models.CharField(blank=True, null=True, max_length=100)
    floor_price = models.IntegerField(blank=True, null=True, default=None)
    max_price = models.IntegerField(blank=True, null=True, default=None)
    num_of_sales = models.IntegerField(blank=True, null=True, default=None)
    num_of_holders = models.IntegerField(blank=True, null=True, default=None)
    twitter_link = models.URLField(blank=True, null=True, max_length=200)
    discord_link = models.URLField(blank=True, null=True, max_length=200)
    collection_web_link = models.URLField(blank=True, null=True, max_length=200)
    search_link = models.URLField(blank=True, null=True, max_length=200)
    open_sea_link = models.URLField(blank=True, null=True, max_length=200)
    abacus_deployment_id = models.CharField(blank=True, null=True, max_length=100)


class NFT(models.Model):
    asset_id = models.IntegerField(blank=False, null=True, default=None, unique=True)
    owner = models.CharField(blank=True, null=True, max_length=100)
    price = models.CharField(blank=True, null=True, max_length=100)
    hash = models.CharField(blank=True, null=True, max_length=100)
    collection_name = models.CharField(blank=True, null=True, max_length=100)


    def __str__(self) -> str:
        return self.asset_id
