# This is the database model developed by amalpullan4@gmail.com
'''
                        List of Table
                        -------------
 Users                  : This table holds the user data which are very important for privacy
 Donations              : Holds the content about all the donations in the platform
 Donation_category      : Stores the details about the category of donations
 Featured               : Holds the content for featured videos
 Products               : Holds the data of products in the store of amarshan
 Categories             : Holds the data about product categories in store
 Notification           : Store the notificaion content
'''

# external dependent modules
from django.db import models
import datetime

def now():
    now_utc             = datetime.datetime.utcnow()
    offset              = datetime.datetime.now() - datetime.datetime.utcnow()
    now_with_offset     = now_utc + offset
    return now_with_offset
# Tables or Models

# User model
class Storage(models.Model):
    media = models.FileField(upload_to='media')
    
    def __str__(self) -> str:
        return self.media
    
class Users(models.Model):
    display_name        = models.CharField(max_length=30)
    email               = models.CharField(max_length=30)
    password            = models.CharField(max_length=200)
    gender              = models.CharField(choices=(('male','male'),('female','female'),('other','other')),max_length=30)
    dob                 = models.CharField(default="",max_length=50)
    profile_url         = models.CharField(max_length=500,default="")
    login_type          = models.CharField(max_length=50,default='google')
    phone_number        = models.CharField(max_length=200,default='')
    joining_date        = models.CharField(default='',max_length=50)
    donations_done      = models.IntegerField(default=0)
    donations_received  = models.IntegerField(default=0)
    building_name       = models.CharField(max_length=50, default='')
    street_name         = models.CharField(max_length=50, default='')
    pincode             = models.IntegerField(default=0)
    city                = models.CharField(max_length=50, default='')
    state               = models.CharField(max_length=50,default='')
    country             = models.CharField(max_length=50,default='')
    landmark            = models.CharField(max_length=100,default='')
    
    def __str__(self) -> str:
        return self.display_name
    
class Login_details(models.Model):
    email               = models.CharField(max_length=100)
    login_time          = models.CharField(default='',max_length=50)
    device              = models.CharField(max_length=800)
    
    def __str__(self) -> str:
        return self.email
    
class Donations(models.Model):
    email_id            = models.CharField(max_length=200,default='')
    platform            = models.CharField(max_length=200,default='')
    profile_url         = models.CharField(max_length=200,default='')
    media_url           = models.CharField(max_length=500)
    media_type          = models.CharField(max_length=20)
    target              = models.IntegerField(default=0)
    current_amount      = models.IntegerField(default=0)
    heart               = models.IntegerField(default=0)
    title               = models.CharField(max_length=100)
    description         = models.CharField(max_length=1000)
    location            = models.CharField(max_length=100,default='')
    donation_type       = models.CharField(max_length=100,default="normal")
    category            = models.CharField(max_length=200,default='')
    upload_on           = models.CharField(max_length=200,default='')
    status              = models.CharField(max_length=200,default='pending',choices=(('pending','pending'),('rejected','rejected'),('running','running'),('completed','completed')))

    def __str__(self) -> str:
        return self.email_id

class Donation_categories(models.Model):    
    name                = models.CharField(max_length=100,default='')
    description         = models.CharField(max_length=500,default='')
    image_url           = models.CharField(max_length=500,default='')
    
    def __str__(self) -> str:
        return self.name
    
class Featured(models.Model):
    media_url            = models.CharField(max_length=500)
    profile_image_url    = models.CharField(max_length=500)
    profile_username     = models.CharField(max_length=100)
    organisation         = models.CharField(max_length=100)
    description          = models.CharField(max_length=200)
    location             = models.CharField(max_length=100)
    running_status       = models.BooleanField(max_length=100,default=False)

    def __str__(self) -> str:
        return self.profile_username
    
# shopping 
'''
Models for storing data of shopping
'''
class Products(models.Model):
    name                = models.CharField(max_length=500,default='')
    category            = models.CharField(max_length=100,default='')
    price               = models.IntegerField(default=0)
    description         = models.CharField(max_length=1000,default='')
    image_1_url         = models.CharField(max_length=300)
    image_2_url         = models.CharField(max_length=300)
    image_3_url         = models.CharField(max_length=300)
    image_4_url         = models.CharField(max_length=300)
    rating              = models.CharField(max_length=30)
    
    def __str__(self) -> str:
        return self.name
    
class Categories(models.Model):
    name                = models.CharField(max_length=200)
    description         = models.CharField(max_length=500,default='')
    image_url           = models.CharField(max_length=500,default='')
    
    def __str__(self) -> str:
        return self.name
    
'''
Models of User alerts
'''

class Notification(models.Model):
    title               = models.CharField(max_length=200)
    message             = models.CharField(max_length=1000)
    
    def __str__(self) -> str:
        return self.title
    
    
class Orders(models.Model):
    email_id            = models.CharField(max_length=500)
    product_name        = models.CharField(max_length=100)
    product_description = models.CharField(max_length=1000)
    product_price       = models.IntegerField()
    order_status        = models.CharField(max_length=100,default='pending',choices=(('delivered','delivered'),('cancelled','cancelled'),('shipping','shipping'),('ordered','ordered'),('processing','processing')))
    product_image_url   = models.CharField(max_length=500)
    item_count          = models.IntegerField()
    ordered_on          = models.CharField(max_length=300,default='')
    
    def __str__(self) -> str:
        return self.email_id
    

class Donation_History(models.Model):
    email_id            = models.CharField(max_length=200,default='')
    media_type          = models.CharField(max_length=20)
    target              = models.IntegerField(default=0)
    heart               = models.IntegerField(default=0)
    title               = models.CharField(max_length=100)
    description         = models.CharField(max_length=1000,default='')
    location            = models.CharField(max_length=100,default='')
    donation_type       = models.CharField(max_length=100,default="")
    category            = models.CharField(max_length=200,default='')
    upload_on           = models.CharField(max_length=100,default='')
    completed_on        = models.CharField(max_length=100,default='')
    
    def __str__(self) -> str:
        return self.email_id
    

class Donation_Payment(models.Model):
    amount              = models.IntegerField()
    public_email_id     = models.CharField(max_length=100)
    user_email_id       = models.CharField(max_length=100)
    user_contact        = models.IntegerField(default=None,null=True)
    # payment_status  = models.CharField(max_length=200,choices=(('')))
    donation_title      = models.CharField(max_length=300)
    donation_id         = models.IntegerField()
    
    def __str__(self) -> str:
        return self.user_email_id
    
class User_Wallet(models.Model):
    amount              = models.IntegerField()
    email               = models.CharField(max_length=100)

    
    def __str__(self) -> str:
        return self.email
    