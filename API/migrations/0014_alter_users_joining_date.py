# Generated by Django 4.1 on 2023-04-21 05:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0013_alter_users_joining_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='joining_date',
            field=models.DateField(default=datetime.datetime(2023, 4, 21, 10, 58, 39, 798034)),
        ),
    ]
