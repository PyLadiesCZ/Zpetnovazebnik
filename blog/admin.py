from django.contrib import admin
from . models import Session, Comment, Course

admin.site.register(Course)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'session', 'course')
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'course', )
