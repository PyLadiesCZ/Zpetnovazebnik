from django.shortcuts import render
from django.utils import timezone
from blog.models import Session, Course
from blog.forms import SessionForm, CommentForm, CourseForm
from django.shortcuts import render, get_object_or_404, redirect
from django.template import Context
from django.http import Http404

import mistune
import os


def course_list(request):
    current_courses = Course.objects.filter(archived=False).filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    past_courses = Course.objects.filter(archived=True).filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    return render(request, 'things/course_list.html', {'current_courses': current_courses, 'past_courses':past_courses})


def session_list(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    sessions = Session.objects.filter(course=course).filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    past_sessions = sessions[1:]
    current_sessions = sessions[:1]
    return render(request, 'things/session_list.html', {'past_sessions': past_sessions, 'current_sessions': current_sessions, 'sessions': sessions, 'course': course})


def session_detail(request, course_slug, session_slug):
    course = get_object_or_404(Course, slug=course_slug)
    session = get_object_or_404(Session, course=course, slug=session_slug)
    if (not session.published_date) or session.published_date<=timezone.now():
        return render(request, 'things/session_detail.html', {'session': session, 'course': course})
    else:
        raise Http404


def add_comment_to_session(request, course_slug, session_slug, password):
    course = get_object_or_404(Course, slug=course_slug)
    session = get_object_or_404(Session, course=course, slug=session_slug)
    if password != course.password:
        raise Http404
    if request.method == "POST":
        form = CommentForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            comment = form.save(commit=False)
            comment.session = session
            comment.course = course
            comment.save()
            return redirect('session_detail', course_slug=course.slug, session_slug=session.slug)
    else:
        form = CommentForm()
    return render(request, 'things/add_comment_to_session.html', {'form': form, 'session':session, 'course':course,})
