from django.contrib import admin

from blog_app.models import UserProfile, Blog

admin.site.register([Blog, UserProfile])