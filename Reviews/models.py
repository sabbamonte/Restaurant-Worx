from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    pass

class Info(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    position = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)

    def serialize(self):
        return {
            "user": self.user,
            "position": self.position,
            "location": self.location
        }
