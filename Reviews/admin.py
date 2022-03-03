from django.contrib import admin

from .models import User, Info

admin.site.register(User)
admin.site.register(Info)