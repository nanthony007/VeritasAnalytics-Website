# Generated by Django 2.1.5 on 2019-05-12 20:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vws_main', '0008_wrestler_eligibility'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fs_match',
            name='gbc4',
        ),
    ]