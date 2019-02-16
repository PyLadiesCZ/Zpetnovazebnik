from django import forms
from .models import Session, Comment, Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('course_name',)


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
