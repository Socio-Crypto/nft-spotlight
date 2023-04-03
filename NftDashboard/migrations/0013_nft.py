# Generated by Django 4.1.2 on 2022-11-01 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("NftDashboard", "0012_rename_address_collection_collection_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="NFT",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("asset_id", models.IntegerField(blank=True, default=None, null=True)),
                ("owner", models.CharField(blank=True, max_length=100, null=True)),
                ("price", models.CharField(blank=True, max_length=100, null=True)),
                ("hash", models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
