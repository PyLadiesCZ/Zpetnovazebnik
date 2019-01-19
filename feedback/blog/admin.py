from django.contrib import admin
from . models import Session, Comment, Course

admin.site.register(Course)
admin.site.register(Session)
admin.site.register(Comment)
