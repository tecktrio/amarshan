# Generated by Django 4.1 on 2023-05-28 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0012_withdraw_requests'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donations',
            name='funding_account',
            field=models.CharField(choices=[('amarshan', 'amarshan'), ('user', 'user')], default='amarshan', max_length=200),
        ),
    ]
