from django.contrib import admin

from .models import Review, User, Info

admin.site.register(User)
admin.site.register(Info)
admin.site.register(Review)