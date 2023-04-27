# Generated by Django 4.1 on 2023-04-27 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(default='', max_length=500)),
                ('image_url', models.CharField(default='', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Donation_categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('description', models.CharField(default='', max_length=500)),
                ('image_url', models.CharField(default='', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Donation_History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_type', models.CharField(max_length=20)),
                ('target', models.IntegerField(default=0)),
                ('heart', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(default='', max_length=1000)),
                ('location', models.CharField(default='', max_length=100)),
                ('donation_type', models.CharField(default='', max_length=100)),
                ('category', models.CharField(default='', max_length=200)),
                ('upload_on', models.CharField(default='', max_length=100)),
                ('completed_on', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Donations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_url', models.CharField(max_length=500)),
                ('media_type', models.CharField(max_length=20)),
                ('target', models.IntegerField(default=0)),
                ('current_amount', models.IntegerField(default=0)),
                ('heart', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1000)),
                ('location', models.CharField(default='', max_length=100)),
                ('donation_type', models.CharField(default='normal', max_length=100)),
                ('category', models.CharField(default='', max_length=200)),
                ('upload_on', models.CharField(default='', max_length=200)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('rejected', 'rejected'), ('running', 'running'), ('completed', 'completed')], default='pending', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Featured',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_url', models.CharField(max_length=500)),
                ('profile_image_url', models.CharField(max_length=500)),
                ('profile_username', models.CharField(max_length=100)),
                ('organisation', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=100)),
                ('running_status', models.BooleanField(default=False, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Login_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=100)),
                ('login_time', models.CharField(default='', max_length=50)),
                ('device', models.CharField(max_length=800)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('message', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_id', models.CharField(max_length=500)),
                ('product_name', models.CharField(max_length=100)),
                ('product_description', models.CharField(max_length=1000)),
                ('product_price', models.IntegerField()),
                ('order_status', models.CharField(choices=[('delivered', 'delivered'), ('cancelled', 'cancelled'), ('shipping', 'shipping'), ('ordered', 'ordered'), ('processing', 'processing')], default='pending', max_length=100)),
                ('product_image_url', models.CharField(max_length=500)),
                ('item_count', models.IntegerField()),
                ('ordered_on', models.CharField(default='', max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=500)),
                ('category', models.CharField(default='', max_length=100)),
                ('price', models.IntegerField(default=0)),
                ('description', models.CharField(default='', max_length=1000)),
                ('image_1_url', models.CharField(max_length=300)),
                ('image_2_url', models.CharField(max_length=300)),
                ('image_3_url', models.CharField(max_length=300)),
                ('image_4_url', models.CharField(max_length=300)),
                ('rating', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female'), ('other', 'other')], max_length=30)),
                ('dob', models.CharField(default='', max_length=50)),
                ('profile_url', models.CharField(default='', max_length=500)),
                ('login_type', models.CharField(default='google', max_length=50)),
                ('phone_number', models.CharField(default='', max_length=200)),
                ('joining_date', models.CharField(default='', max_length=50)),
                ('donations_done', models.IntegerField(default=0)),
                ('donations_received', models.IntegerField(default=0)),
                ('building_name', models.CharField(default='', max_length=50)),
                ('street_name', models.CharField(default='', max_length=50)),
                ('pincode', models.IntegerField(default=0)),
                ('city', models.CharField(default='', max_length=50)),
                ('state', models.CharField(default='', max_length=50)),
                ('country', models.CharField(default='', max_length=50)),
                ('landmark', models.CharField(default='', max_length=100)),
            ],
        ),
    ]