from atexit import register
from django.contrib import admin
from .models import Follow, Profile, Project, Rating

# Register your models here.
admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Follow)
admin.site.register(Rating)