from django.contrib import admin
from .models import Instance, UserProfile, Project, Csv, Preference, Allocation

# Register your models here.
admin.site.register(Instance)
admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(Csv)
admin.site.register(Preference)
admin.site.register(Allocation)