from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator


# Create your models here.
class User(AbstractUser):
    pass

class Info(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    position = models.CharField(max_length=200, blank=True)

    def serialize(self):
        return {
            "user": self.user,
            "position": self.position,
            "location": self.location
        }

class Review(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, default=None)
    zip = models.PositiveIntegerField(blank=False, validators=[MaxValueValidator(99950)], default=None)
    position = models.CharField(max_length=200)
    days = models.PositiveIntegerField()
    hours = models.FloatField()
    pay = models.PositiveIntegerField()
    slow = models.PositiveIntegerField()
    busy = models.PositiveIntegerField()
    envo = models.PositiveIntegerField()
    mngmt = models.PositiveIntegerField()
    comments = models.CharField(max_length=500)
    rating = models.PositiveIntegerField()

