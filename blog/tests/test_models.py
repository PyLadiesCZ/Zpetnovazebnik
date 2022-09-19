from pathlib import Path
import datetime

import pytest
from django.utils.timezone import now
from datetime import timezone
from betamax import Betamax
import requests

from blog.models import Course, Session


with Betamax.configure() as config:
    config.cassette_library_dir = Path(__file__).parent / 'fixtures/cassettes'

@pytest.fixture
def course():
    course = Course(course_name='My course', slug='my-course')
    course.full_clean()
    return course


@pytest.mark.django_db
def test_course_basic_attributes(course):
    assert course.course_name == 'My course'
    assert course.slug == 'my-course'
    assert type(course.password) == str
    assert len(course.password) > 4
    assert course.published_date == None
    assert course.text == None
    assert course.archived == False


@pytest.mark.django_db
def test_course_publish(course):
    course.publish()
    assert course.published_date <= now()


@pytest.mark.django_db
def test_course_adjust_naucse_url(course):
    course.naucse_slug = 'https://naucse.python.cz/2020/brno-jaro-pondeli/'
    course.clean_fields()
    assert course.naucse_slug == '2020/brno-jaro-pondeli'


@pytest.mark.django_db
@pytest.mark.parametrize('slug', [
    '2019/brno-podzim-pondeli',
    'https://naucse.python.cz/2019/brno-podzim-pondeli/',
])
def test_course_create_from_naucse(slug):
    messages = []
    session = requests.Session()
    with Betamax(session).use_cassette('course'):
        course = Course.create_from_naucse(
            slug, messages.append,
            session=session,
        )
    print(messages)
    assert course.course_name == (
        'Začátečnický kurz PyLadies – Brno - podzim 2019 - pondělí')
    sessions = list(course.sessions.all())
    assert len(sessions) == 12

    first_session = course.sessions.get(slug='expressions')
    assert first_session.title == 'Lekce 1'
    assert first_session.text == 'Výrazy a podmínky'
    assert first_session.published_date == datetime.datetime(
        2019, 9, 23, 16, 0, tzinfo=timezone.utc
    )


@pytest.mark.django_db
def test_course_update_from_naucse(course):
    messages = []
    course.naucse_slug = '2019/brno-podzim-pondeli'
    course.save()

    # An extra session, not present on naucse
    extra_session = Session(
        title='Extra session',
        slug='extra',
        course=course,
    )
    extra_session.save()

    # Add session with slug on naucse, with old data
    extra_session = Session(
        title='Old title',
        text='Old text',
        slug='expressions',
        published_date=datetime.datetime(
            2000, 1, 1, 1, 1, tzinfo=timezone.utc
        ),
        course=course,
    )
    extra_session.save()

    session = requests.Session()
    with Betamax(session).use_cassette('course'):
        course.update_from_naucse(
            messages.append,
            session=session,
        )
    print(messages)
    assert course.course_name == (
        'Začátečnický kurz PyLadies – Brno - podzim 2019 - pondělí')

    sessions = list(course.sessions.all())
    assert len(sessions) == 13

    # An extra session should be preserved
    extra_session = course.sessions.get(slug='extra')
    assert extra_session.title == 'Extra session'

    # Session with slug on naucse should be updated
    first_session = course.sessions.get(slug='expressions')
    assert first_session.title == 'Lekce 1'
    assert first_session.text == 'Výrazy a podmínky'
    assert first_session.published_date == datetime.datetime(
        2019, 9, 23, 16, 0, tzinfo=timezone.utc
    )

    # Session from naucse should be added
    second_session = course.sessions.get(slug='cycles')
    assert second_session.title == 'Lekce 2'
    assert second_session.text == 'Funkce a cykly'
    assert second_session.published_date == datetime.datetime(
        2019, 9, 30, 16, 0, tzinfo=timezone.utc
    )
