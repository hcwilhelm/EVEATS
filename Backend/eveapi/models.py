#  models.py
#  EVEARS
#  
#  Created by Hans Christian Wilhelm on 2011-09-05.
#  Copyright 2011 scienceondope.org All rights reserved.
# 

from django.db import models
from django.contrib.auth.models import User

import datetime

# ============================================================================================
# = APIKeyInfo see  http://wiki.eve-id.net/APIv2_Account_APIKeyInfo_XML                      =
# ============================================================================================

class APIKeyInfo(models.Model):
  accessMask      = models.IntegerField(null=False)
  accountType     = models.CharField(max_length=64, null=False)
  expires         = models.DateTimeField(null=True)
  cachedUntil     = models.DateTimeField(null=False)
  
  def expired(self):
    return self.cachedUntil < datetime.datetime.utcnow()

# ============================================================================================
# = Class APIKey. Note ! Before accesing related models you should call the importTasks      =
# ============================================================================================

class APIKey(models.Model):
  keyID           = models.IntegerField(null=False)
  vCode           = models.CharField(max_length=64, null=False)
  name            = models.CharField(max_length=128)
  user            = models.ForeignKey(User)
  apiKeyInfo      = models.ForeignKey(APIKeyInfo, null=True)

# =============================================================================================
# = Class Characters                                                                          =
# =============================================================================================

class Characters(models.Model):
  characterID     = models.IntegerField(primary_key=True)
  characterName   = models.CharField(max_length=128, null=False)
  corporationID   = models.IntegerField(null=False)
  corporationName = models.CharField(max_length=128, null=False)
  cachedUntil     = models.DateTimeField(null=False)
  apiKey          = models.ForeignKey(APIKey, null=False)

  def expired(self):
    return self.cachedUntil < datetime.datetime.utcnow()