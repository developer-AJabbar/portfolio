from django.contrib import admin
from .models import Profile, Skill, Project, Resume

admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Resume)