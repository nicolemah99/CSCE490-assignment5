# Generated by Django 4.1.2 on 2022-10-19 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_alter_listing_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='price',
            new_name='startingBid',
        ),
    ]