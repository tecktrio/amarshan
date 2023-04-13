# Generated by Django 4.1 on 2023-04-13 13:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0006_rename_first_name_users_display_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='login_type',
            field=models.CharField(default='google', max_length=50),
        ),
        migrations.AddField(
            model_name='users',
            name='profile_url',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='users',
            name='joining_date',
            field=models.DateField(default=datetime.datetime(2023, 4, 13, 19, 1, 37, 187621)),
        ),
    ]
