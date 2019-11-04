from django.contrib import admin

from .models import Allergy, Child, Post, Home

admin.site.register(Allergy)
admin.site.register(Child)
admin.site.register(Post)
admin.site.register(Home)