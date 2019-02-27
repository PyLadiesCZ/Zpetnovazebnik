import datetime

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
import requests
import pytz

from blog.models import Course, Session

URL_TEMPLATE = 'https://naucse.python.cz/v0/{}.json'



def parse_datetime(date_string):
    """Get a datetime object from a string value"""
    try:
        return datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S%z')
    except ValueError:
        result = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        # Workaround for https://github.com/pyvec/naucse.python.cz/issues/525
        return pytz.timezone('Europe/Prague').localize(result)



class Command(BaseCommand):
    help = 'Import (or re-import) a course from Naucse API'

    def add_arguments(self, parser):
        parser.add_argument('course_slug', type=str)

    def handle(self, *args, **options):
        course_slug = options['course_slug']
        url = URL_TEMPLATE.format(course_slug)
        print(f'Getting {url}...')
        response = requests.get(url)
        response.raise_for_status()
        course_info = response.json()['course']
        course_slug = course_slug.replace('/', '-')
        course, created = Course.objects.get_or_create(slug=course_slug)
        if created:
            print(f'Added {course!r}')
            course.published_date = timezone.now()
        else:
            print(f'Updating {course!r}')
        if 'subtitle' in course_info:
            course.course_name = f"{course_info['title']} – {course_info['subtitle']}"
        else:
            course.course_name = course_info['title']
        course.save()

        for session_info in course_info['sessions']:
            if 'time' not in session_info:
                print(f'Skipping session without time: {session_info["title"]}')
            else:
                session, created = Session.objects.get_or_create(
                    course=course,
                    slug=session_info['slug'],
                )
                if created:
                    print(f'Added {session!r}')
                else:
                    print(f'Updating {session!r}')
                if 'serial' in session_info:
                    session.title = f'Lekce {session_info["serial"]}'
                else:
                    session.title = None
                session.text = session_info['title']
                published_date = parse_datetime(session_info['time']['start'])
                session.published_date = published_date
                session.save()
