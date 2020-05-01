import contextlib

from django.contrib import admin
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.urls import path, reverse
from django.shortcuts import redirect
from django.utils import timezone

from . models import Session, Comment, Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'naucse_slug', 'is_published')
    search_fields = ['course_name', 'slug']
    actions = ['update_from_naucse']
    prepopulated_fields = {"slug": ("course_name",)}
    change_list_template = 'things/admin_course_change_list.html'

    def is_published(self, course):
        if not course.published_date:
            return '—'
        if course.published_date < timezone.now():
            return '✓'
        else:
            return '—'
    is_published.short_description = 'Published'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                'add_from_naucse/',
                self.admin_site.admin_view(self.add_fromnaucse_view),
                name='blog_course_add_from_naucse',
            ),
        ]
        return my_urls + urls

    def update_from_naucse(self, request, queryset):
        for course in queryset:
            reports = []
            try:
                course.update_from_naucse(reports.append)
            except ValueError as e:
                self.msg(request, str(e), messages.WARNING)
                self.msg(request, reports)
            else:
                self.msg(request, reports)
    update_from_naucse.short_description = 'Aktualizovat podle naucse'

    def msg(self, request, msg, level=messages.INFO):
        """Add a message to the user

        Message can be a list; if it is, it's shown as several lines.
        """
        if isinstance(msg, list):
            msg = mark_safe('<br>'.join(escape(r) for r in msg))
        self.message_user(request, msg, level=level)

    def add_fromnaucse_view(self, request):
        """View for the 'add_from_naucse' action"""
        if request.method == 'POST':
            reports = []
            slug = request.POST['slug']
            if not slug:
                self.message_user(
                    request, 'no naucse slug given', level=messages.ERROR,
                )
                return redirect(reverse('admin:blog_course_changelist'))
            reports = []
            try:
                course = Course.create_from_naucse(slug, reports.append)
            except ValueError as e:
                self.msg(request, str(e), messages.WARNING)
                self.msg(request, reports)
            else:
                self.msg(request, reports)
                self.msg(
                    request, 'Nezapomeň nastavit "Published date"!',
                    messages.WARNING
                )
                return redirect(reverse(
                    'admin:blog_course_change', args=[course.id],
                ))
            return redirect(reverse('admin:blog_course_changelist'))
        else:
            return HttpResponseNotAllowed(['POST'])


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'session', 'course')

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'course', )
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ['course']
