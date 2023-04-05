from django.db import models

# Create your models here.

class Users(models.Model):
    username = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    gender = models.CharField(choices=(('male','male'),('female','female'),('other','other')),max_length=30)
    dob = models.DateField()
    user_id = models.IntegerField()
    donations_done = models.IntegerField()
    donations_received = models.IntegerField()
    
class Donations(models.Model):
    media_url = models.CharField(max_length=500)
    media_type = models.CharField(max_length=20)
    target = models.IntegerField()
    current_amount = models.IntegerField(default=0)
    heart = models.IntegerField(default=0)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    donation_type = models.CharField(max_length=100,default="normal")
    
class Featured(models.Model):
    media_url = models.CharField(max_length=500)
    profile_image_url = models.CharField(max_length=500)
    profile_username = models.CharField(max_length=100)
    organisation = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    running_status = models.BooleanField(max_length=100,default=False)

