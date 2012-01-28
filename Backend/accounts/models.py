from django.db import models
from django.contrib.auth.models import User

class AccountProfile(models.Model):
    user        = models.OneToOneField(User)