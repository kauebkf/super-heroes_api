from django.contrib import admin

from .models import User, Hero, SuperPower

admin.site.register(User)
admin.site.register(Hero)
admin.site.register(SuperPower)
