from django.contrib import admin

from API_backend.API.models import Donations, Users

# Register your models here.
admin.site.register(Users)
admin.site.register(Donations)
