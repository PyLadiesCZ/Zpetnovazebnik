from django.db import models
from django.utils import timezone


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    published_date = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=10)
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def __str__(self):
        return self.course_name


class Session(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sessions')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def __str__(self):
        return self.title

class Comment(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='comments')
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
