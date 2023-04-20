from django.contrib import admin

from API.models import Donations, Featured, Users

# Register your models here.
admin.site.register(Users)
admin.site.register(Donations)
admin.site.register(Featured)
