#  models.py
#  EVEARS
#  
#  Created by Hans Christian Wilhelm on 2011-09-05.
#  Copyright 2011 scienceondope.org All rights reserved.
# 


from django.db import models
from django.contrib.auth.models import User

class EveApiKey(models.Model):
    ccpID               = models.IntegerField(null=False)
    verificationCode    = models.CharField(max_length=128, null=False)
    comment             = models.CharField(max_length=512, null=True)
    owner               = models.ForeignKey(User)