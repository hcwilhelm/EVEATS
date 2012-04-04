#  models.py
#  EVEARS
#  
#  Created by Hans Christian Wilhelm on 2011-09-05.
#  Copyright 2011 scienceondope.org All rights reserved.
# 

from django.db import models
from django.contrib.auth.models import User

from evedb.models import *

import datetime


# =============================================================================================
# = /account/APIKeyInfo.xml.aspx                                                              =
# =============================================================================================

class APIKeyInfo(models.Model):
  currentTime       = models.DateTimeField()
  accessMask        = models.IntegerField()
  accountType       = models.CharField(max_length=255)
  expires           = models.DateTimeField(null=True)
  cachedUntil       = models.DateTimeField()
  
  def expired(self):
    return self.cachedUntil < datetime.datetime.utcnow()
  
class Characters(models.Model):
  characterID       = models.IntegerField()
  characterName     = models.CharField(max_length=255)
  corporationID     = models.IntegerField()
  corporationName   = models.CharField(max_length=255)
  apiKeyInfo        = models.ForeignKey('APIKeyInfo')

# =============================================================================================
# = /char/AssetList.xml.aspx                                                                  =
# =============================================================================================

class AssetList(models.Model):
  character         = models.ForeignKey('Characters')
  currentTime       = models.DateTimeField()
  cachedUntil       = models.DateTimeField()
  
  def expired(self):
     return self.cachedUntil < datetime.datetime.utcnow()
  
class Assets(models.Model):
  assetList         = models.ForeignKey(AssetList)
  parent            = models.ForeignKey('self', null=True, blank=True)
  itemID            = models.BigIntegerField()
  locationID        = models.ForeignKey('evedb.mapDenormalize', null=True, blank=True)
  typeID            = models.ForeignKey('evedb.invTypes')
  quantity          = models.IntegerField()
  flag              = models.ForeignKey('evedb.invFlags')
  singleton         = models.BooleanField()
  rawQuantity       = models.IntegerField(null=True, blank=True)
  

# ============================================================================================
# = Class APIKey. Note ! Before accesing related models you should call the updateTasks      =
# ============================================================================================

class APIKey(models.Model):
  keyID           = models.IntegerField(null=False)
  vCode           = models.CharField(max_length=64, null=False)
  name            = models.CharField(max_length=128)
  user            = models.ForeignKey(User)
  apiKeyInfo      = models.ForeignKey(APIKeyInfo, null=True, on_delete=models.SET_NULL)
  