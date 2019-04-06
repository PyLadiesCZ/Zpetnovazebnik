import secrets

from django.db import models
from django.utils import timezone


def make_random_password():
    return secrets.token_urlsafe(8)

    
class Course(models.Model):
    course_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, unique=True)
    text = models.TextField(help_text="Pokud pole zůstane prázdné, vloží se automaticky obecný text k PyLadies kurzům", blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)
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
        else:
            return self.text

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
