from django.db import models
import datetime
# Create your models here.

class Users(models.Model):
    display_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    gender = models.CharField(choices=(('male','male'),('female','female'),('other','other')),max_length=30)
    dob = models.CharField(default="",max_length=50)
    profile_url = models.CharField(max_length=500,default="")
    login_type = models.CharField(max_length=50,default='google')
    joining_date = models.DateField()
    donations_done = models.IntegerField(default=0)
    donations_received = models.IntegerField(default=0)
    building_name = models.CharField(max_length=50, default='')
    street_name = models.CharField(max_length=50, default='')
    pincode = models.IntegerField(default=0)
    city = models.CharField(max_length=50, default='')
    state = models.CharField(max_length=50,default='')
    country = models.CharField(max_length=50,default='')
    
class Donations(models.Model):
    media_url = models.CharField(max_length=500)
    media_type = models.CharField(max_length=20)
    target = models.IntegerField()
    current_amount = models.IntegerField(default=0)
    heart = models.IntegerField(default=0)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    location = models.CharField(max_length=100)
    donation_type = models.CharField(max_length=100,default="normal")
    category = models.CharField(max_length=200,default='')
    status = models.CharField(max_length=200,default='pending',choices=(('pending','pending'),('approved','approved'),('not_approved','not_approved')))

class Donation_categories(models.Model):    
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    
class Featured(models.Model):
    media_url = models.CharField(max_length=500)
    profile_image_url = models.CharField(max_length=500)
    profile_username = models.CharField(max_length=100)
    organisation = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    running_status = models.BooleanField(max_length=100,default=False)


#shopping 
class Products(models.Model):
    name = models.CharField(max_length=100,default='')
    category = models.CharField(max_length=100,default='')
    price = models.IntegerField(max_length=50,default=0)
    description = models.CharField(max_length=800,default='')
    image_1_url = models.CharField(max_length=300)
    image_2_url = models.CharField(max_length=300)
    image_3_url = models.CharField(max_length=300)
    image_4_url = models.CharField(max_length=300)
    rating = models.CharField(max_length=30)
    
    
class Categories(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500,default='')
    
class Notification(models.Model):
    title = models.CharField(max_length=200)
    message = models.CharField(max_length=1000)