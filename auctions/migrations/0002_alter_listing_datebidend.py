# Generated by Django 4.1.2 on 2022-10-24 22:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='dateBidEnd',
            field=models.DateField(default=datetime.date(2022, 10, 31), verbose_name='End Date'),
        ),
    ]
