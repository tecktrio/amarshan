# Generated by Django 4.1 on 2023-04-30 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation_history',
            name='email_id',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='donations',
            name='email_id',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='donations',
            name='profile_url',
            field=models.CharField(default='', max_length=200),
        ),
    ]
