from django.db import models
from django.contrib.auth.models import User

class AccountDetails(models.Model):
    user            = models.OneToOneField(User)
    icqNumber       = models.CharField(max_length=16)
    jabberAccount   = models.CharField(max_length=64)
