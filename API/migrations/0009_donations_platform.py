# Generated by Django 4.1 on 2023-05-03 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0008_alter_users_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='donations',
            name='platform',
            field=models.CharField(default='', max_length=200),
        ),
    ]
