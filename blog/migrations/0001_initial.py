# Generated by Django 2.1.5 on 2019-02-04 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('title', models.CharField(max_length=250, primary_key=True, serialize=False, unique=True)),
                ('content', models.FileField(upload_to='')),
                ('date', models.DateField(auto_now_add=True)),
                ('slug', models.SlugField(default=models.CharField(max_length=250, primary_key=True, serialize=False, unique=True))),
            ],
        ),
    ]
