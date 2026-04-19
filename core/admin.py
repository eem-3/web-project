from django.contrib import admin
from .models import Status, Tag, Entity, Media, Project, Comment, Report

# Register your models here.
admin.site.register(Status)
admin.site.register(Tag)
admin.site.register(Entity)
admin.site.register(Media)
admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(Report)