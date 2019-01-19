from django.shortcuts import render
from django.utils import timezone
from blog.models import Session, Course
from blog.forms import SessionForm, CommentForm, CourseForm
from django.shortcuts import render, get_object_or_404, redirect
from django.template import Context
from django.http import Http404
import os


def course_list(request):
    courses = Course.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    return render(request, 'things/course_list.html', {'courses': courses})

def session_list(request, course_name):
    course = get_object_or_404(Course, course_name=course_name)
    sessions = Session.objects.filter(course=course) #.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    past_sessions = sessions[1:]
    current_sessions = sessions[:1]

    return render(request, 'things/session_list.html', {'past_sessions': past_sessions, 'current_sessions': current_sessions, 'sessions': sessions, 'course': course})

def session_detail(request, course_name, pk):
    course = get_object_or_404(Course, course_name=course_name)
    session = get_object_or_404(Session, pk=pk)
    if (not session.published_date) or session.published_date<=timezone.now():
        return render(request, 'things/session_detail.html', {'session': session, 'course': course})
    else:
        raise Http404

def add_comment_to_session(request, course_name, pk):
    course = get_object_or_404(Course, course_name=course_name)
    session = get_object_or_404(Session, pk=pk)
    if request.method == "session":
        form = CommentForm(request.session)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.session = session
            comment.save()
            return redirect('session_detail', course_name=course.course_name, pk=session.pk)
    else:
        form = CommentForm()
    return render(request, 'things/add_comment_to_session.html', {'form': form, 'session':session, 'course':course})
