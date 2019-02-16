from django.db import migrations, models
from django.utils.text import slugify

from blog.models import Session


def fill_slug(apps, schema_editor):
    for session in Session.objects.all():
        session.slug = slugify(session.title)
        session.save()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='slug',
            field=models.SlugField(default='', max_length=250),
            preserve_default=False,
        ),
        migrations.RunPython(
            fill_slug,
            migrations.RunPython.noop,
        ),
        migrations.AlterUniqueTogether(
            name='session',
            unique_together={('course', 'slug')},
        ),
    ]
