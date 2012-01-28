#  models.py
#  EVEARS
#  
#  Created by Hans Christian Wilhelm on 2011-09-05.
#  Copyright 2011 scienceondope.org All rights reserved.
# 


from django.db import models
from django.contrib.auth.models import User

class EveApiKey(models.Model):
    ID                  = models.BigIntegerField(primary_key=True)
    verificationCode    = models.CharField(max_length=128)
    comment             = models.CharField(max_length=512)
    owner               = models.ForeignKey(User)