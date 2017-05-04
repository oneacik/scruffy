import hashlib

from django.db import models


class Project(models.Model):
    _choices = [(False, 'private'), (True, 'public')]
    project_name = models.CharField(max_length=16, help_text="Title displayed on main page",
                                    unique=True)
    description = models.TextField(help_text="First 50 letters will be on projects page")
    privacy = models.BooleanField(choices=_choices,
                                  help_text="Private for invitation only - anyone can join public projects")
    people_limit = models.IntegerField(help_text="0 for no limit for project - limit for hakaton is 60 people")
    email = models.EmailField(help_text="Email used for project activision")
    active = models.BooleanField(default=False)
    time = models.DateTimeField(null=True)

class Hacker(models.Model):
    email = models.EmailField(unique=True)
    time = models.DateTimeField(null=True)
    project = models.ForeignKey(Project, null=True)