# Generated by Django 4.1 on 2023-04-25 07:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0023_alter_login_details_login_time_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_id', models.CharField(max_length=500)),
                ('product_id', models.IntegerField()),
                ('product_name', models.CharField(max_length=100)),
                ('product_description', models.CharField(max_length=1000)),
                ('product_price', models.IntegerField()),
                ('order_status', models.CharField(default='pending', max_length=100)),
                ('product_image_url', models.CharField(max_length=500)),
            ],
        ),
        migrations.AddField(
            model_name='donation_categories',
            name='image_url',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='users',
            name='landmark',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='donation_categories',
            name='description',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='donation_categories',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='donations',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('rejected', 'rejected'), ('running', 'running'), ('completed', 'completed')], default='pending', max_length=200),
        ),
        migrations.AlterField(
            model_name='login_details',
            name='device',
            field=models.CharField(max_length=800),
        ),
        migrations.AlterField(
            model_name='login_details',
            name='login_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 25, 13, 6, 18, 408793)),
        ),
        migrations.AlterField(
            model_name='users',
            name='joining_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 25, 13, 6, 18, 408793)),
        ),
    ]
