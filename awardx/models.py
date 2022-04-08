from distutils.command.upload import upload
from pyexpat import model
from turtle import title
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    """Model definition for Profile."""

    # TODO: Define fields here
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to = 'awwwards/static/images/profiles/')
    bio = models.TextField()
    my_link = models.URLField()

    class Meta:
        """Meta definition for Profile."""

        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        """Unicode representation of Profile."""
        return str(self.user)

class Project(models.Model):
    """Model definition for Project."""

    # TODO: Define fields here
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    image = models.ImageField(upload_to = 'awwwards/static/images/projects/')
    description = models.TextField()
    link = models.URLField()

    class Meta:
        """Meta definition for Project."""

        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        """Unicode representation of Project."""
        pass

