# Generated by Django 2.1.7 on 2019-04-06 13:16

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_course_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='password',
            field=models.CharField(default=blog.models.make_random_password, help_text='Heslo se generuje automaticky, ale je možné vyplnit vlastní. Slouží jako součást URL pro zadávání zpětné vazby.', max_length=50),
        ),
        migrations.AlterField(
            model_name='course',
            name='text',
            field=models.TextField(blank=True, help_text='Pokud pole zůstane prázdné, vloží se automaticky obecný text k PyLadies kurzům', null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='text',
            field=models.TextField(blank=True, help_text="Pokud vyplníš toto políčko, jeho obsah se zobrazí jako součást názvu za obsahem políčka 'Title'", null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='title',
            field=models.CharField(blank=True, help_text="Pokud políčko zůstane prázdné, použije se jako název obsah pole 'Text'", max_length=200, null=True),
        ),
    ]
