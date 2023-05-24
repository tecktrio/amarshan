from django.contrib import admin

from API.models import Donations, Featured, Users, Bank_Accounts
from API.models import Storage

# Register your models here.
admin.site.register(Users)
admin.site.register(Donations)
admin.site.register(Featured)
admin.site.register(Storage)
admin.site.register(Bank_Accounts)
