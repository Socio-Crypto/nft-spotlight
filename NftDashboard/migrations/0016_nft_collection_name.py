# Generated by Django 4.1.2 on 2022-11-01 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NftDashboard', '0015_alter_nft_asset_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='nft',
            name='collection_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
