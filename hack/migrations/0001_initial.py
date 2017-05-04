# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-05-04 01:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hacker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('time', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(help_text='Title displayed on main page', max_length=16, unique=True)),
                ('description', models.TextField(help_text='First 50 letters will be on projects page')),
                ('privacy', models.BooleanField(choices=[(False, 'private'), (True, 'public')], help_text='Private for invitation only - anyone can join public projects')),
                ('people_limit', models.IntegerField(help_text='0 for no limit for project - limit for hakaton is 60 people')),
                ('email', models.EmailField(help_text='Email used for project activision', max_length=254)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='hacker',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hack.Project'),
        ),
    ]
