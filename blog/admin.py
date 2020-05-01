from django.contrib import admin
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.utils.html import escape

from . models import Session, Comment, Course


def update_from_naucse(modeladmin, request, queryset):
    for course in queryset:
        reports = []
        try:
            course.update_from_naucse(reports.append)
        except ValueError as e:
            reports.append(str(e))
            level = messages.WARNING
        else:
            level = messages.INFO
        modeladmin.message_user(
            request,
            mark_safe('<br>'.join(escape(r) for r in reports)),
            level=level,
        )
update_from_naucse.short_description = 'Aktualizovat podle naucse'


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'naucse_slug')
    search_fields = ['course_name', 'slug']
    actions = [update_from_naucse]
    prepopulated_fields = {"slug": ("course_name",)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'session', 'course')

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'course', )
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ['course']
