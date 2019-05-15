# Generated by Django 2.1.5 on 2019-05-12 18:33

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('vws_main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fs_team',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=('abbreviation',), unique=True, verbose_name='slug'),
        ),
    ]
