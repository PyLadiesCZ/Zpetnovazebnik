from django.core.management.base import BaseCommand

from blog.models import Course


class Command(BaseCommand):
    help = 'Import (or re-import) a course from Naucse API'

    def add_arguments(self, parser):
        parser.add_argument('course_slug', type=str)

    def handle(self, *args, **options):
        course_slug = options['course_slug']
        course_slug = course_slug.replace('/', '-')
        course, created = Course.objects.get_or_create(slug=course_slug)
        if created:
            print(f'Added {self!r}')
            course.naucse_slug = options['course_slug']

        course.update_from_naucse(print)
