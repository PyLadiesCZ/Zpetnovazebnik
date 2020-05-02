import secrets
import re
import datetime

from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.utils import timezone
import requests
import pytz

NAUCSE_API_URL_TEMPLATE = 'https://naucse.python.cz/v0/{}.json'
NAUCSE_URL_RE = re.compile('https://naucse\.python\.cz/([^/]+/[^/]+)/?')

def make_random_password():
    return secrets.token_urlsafe(8)

class NaucseSlugField(models.CharField):
    """Slug of a naucse course.

    As part of validation, naucse URLs are reduced to the slug.
    """
    default_validators = [RegexValidator('[-_a-z0-9/]+')]

    @staticmethod
    def to_python(value):
        if not value:
            return None
        match = NAUCSE_URL_RE.match(value)
        if match:
            value = match[1]
        return value


def parse_datetime(date_string):
    """Get a datetime object from a string value"""
    try:
        return datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S%z')
    except ValueError:
        result = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        # Workaround for https://github.com/pyvec/naucse.python.cz/issues/525
        return pytz.timezone('Europe/Prague').localize(result)


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, unique=True)
    text = models.TextField(help_text="Pokud pole zůstane prázdné, vloží se automaticky obecný text k PyLadies kurzům", blank=True, null=True)
    naucse_slug = NaucseSlugField(max_length=500, help_text="Pokud je vyplněno, kurz bude propojen s daným kurzem na naucse.", blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)
    archived = models.BooleanField(default=False)
    password = models.CharField(help_text="Heslo se generuje automaticky, ale je možné vyplnit vlastní. Slouží jako součást URL pro zadávání zpětné vazby.", max_length=50, default=make_random_password)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        if self.slug == None:
            self.slug = slugify(self.name, allow_unicode=True)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.course_name

    @classmethod
    def create_from_naucse(cls, slug, report_progress=print):
        """Create a new course given a slug (or URL) for naucse

        Calls the `report_progress` function with status updates.
        Raises ValueError on failure.
        """
        naucse_slug = NaucseSlugField.to_python(slug)
        course_slug = naucse_slug.replace('/', '-')
        course, created = Course.objects.get_or_create(
            slug=course_slug,
        )
        if created:
            course.naucse_slug = naucse_slug
        else:
            raise ValueError(f'Course exists: {course_slug}')

        try:
            course.update_from_naucse(report_progress)
        except:
            course.delete()
            raise
        return course

    def update_from_naucse(self, report_progress=print):
        """Sync this course with naucse.

        Updates course name.
        Updates sessions whose slugs match naucse.
        Adds new sessions.
        Does *not* delete existing sessions. (There can be feedback for
        extra sessions that aren't on naucse.)

        Calls the `report_progress` function with status updates.
        Raises ValueError on failure (e.g. course without naucse slug).
        """
        if self.naucse_slug == None:
            raise ValueError(f'No naucse slug for course {self.course_name}')
        url = NAUCSE_API_URL_TEMPLATE.format(self.naucse_slug)
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f'Could not update course: {url} returned {response.status_code}')
        response.raise_for_status()
        course_info = response.json()['course']
        if 'subtitle' in course_info:
            self.course_name = f"{course_info['title']} – {course_info['subtitle']}"
        else:
            self.course_name = course_info['title']

        report_progress(f'Updating {self!r}')

        self.save()

        for session_info in course_info['sessions']:
            if 'time' not in session_info:
                report_progress(
                    f'Skipping session without time: {session_info["title"]}')
            else:
                session, created = Session.objects.get_or_create(
                    course=self,
                    slug=session_info['slug'],
                )
                if 'serial' in session_info:
                    session.title = f'Lekce {session_info["serial"]}'
                else:
                    session.title = None
                session.text = session_info['title']
                published_date = parse_datetime(session_info['time']['start'])
                session.published_date = published_date

                if created:
                    report_progress(f'Added {session!r}')
                else:
                    report_progress(f'Updating {session!r}')

                self.save()


class Session(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sessions')
    title = models.CharField(help_text="Pokud políčko zůstane prázdné, použije se jako název obsah pole 'Text'", max_length=200, blank=True, null=True)
    text = models.TextField(help_text="Pokud vyplníš toto políčko, jeho obsah se zobrazí jako součást názvu za obsahem políčka 'Title'", blank=True, null=True)
    slug = models.SlugField(max_length=250)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def __str__(self):
        if self.title:
            return self.title
        elif self.text:
            return self.text
        else:
            return '(no title)'

    class Meta:
        unique_together = ("course", "slug")


class Comment(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='comments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sessions_comments')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    def approve(self):
        self.approved_comment = True
        self.save()
    def create(self):
        self.created_date = timezone.now()
        self.save()
    def __str__(self):
        return self.text
