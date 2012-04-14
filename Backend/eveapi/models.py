#  models.py
#  EVEARS
#
#  Created by Hans Christian Wilhelm on 2011-09-05.
#  Copyright 2011 scienceondope.org All rights reserved.
#

from django.db import models
from django.contrib.auth.models import User
from evedb.models import *
from django.core.cache import cache
import datetime
import logging
logger = logging.getLogger(__name__)

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

class CharacterAPIKeys(models.Model):
  apiKeyInfo        = models.ForeignKey('APIKeyInfo')
  character         = models.ForeignKey('Character')

# =============================================================================================
# = General eve stuff                                                                         =
# =============================================================================================

class Alliance(models.Model):
  allianceID        = models.IntegerField(primary_key=True)
  allianceName      = models.CharField(max_length=255)

class Corporation(models.Model):
  corporationID     = models.IntegerField(primary_key=True)
  corporationName   = models.CharField(max_length=255)
  ceo               = models.ForeignKey('Character', null=True)
  description       = models.TextField(null=True)
  cachedUntil       = models.DateTimeField(default=datetime.datetime.utcnow(), blank=True)
  alliances         = models.ManyToManyField('Alliance', through='CorporationAllianceHistory')
  apikeys           = models.ManyToManyField('APIKeyInfo', through='CharacterAPIKeys')

  def expired(self):
    return self.cachedUntil < datetime.datetime.utcnow()

class Character(models.Model):
  characterID       = models.IntegerField(primary_key=True)
  characterName     = models.CharField(max_length=255)
  securityStatus    = models.DecimalField(decimal_places=16, max_digits=18, null=True)
  race              = models.CharField(max_length=64, null=True)
  bloodline         = models.CharField(max_length=64, null=True)
  isDeleted         = models.BooleanField(default=0)
  cachedUntil       = models.DateTimeField(default=datetime.datetime.utcnow(), blank=True)
  corporations      = models.ManyToManyField('Corporation', through='CharacterEmploymentHistory')

  def expired(self):
    return self.cachedUntil < datetime.datetime.utcnow()

class CharacterEmploymentHistory(models.Model):
  character         = models.ForeignKey('Character')
  corporation       = models.ForeignKey('Corporation')
  startDate         = models.DateTimeField()

class CorporationAllianceHistory(models.Model):
  corporation       = models.ForeignKey('Corporation')
  alliance          = models.ForeignKey('Alliance')
  startDate         = models.DateTimeField()

# =============================================================================================
# = /char/AssetList.xml.aspx                                                                  =
# =============================================================================================

class AssetList(models.Model):
  character         = models.ForeignKey('Character')
  currentTime       = models.DateTimeField()
  cachedUntil       = models.DateTimeField()

  def expired(self):
     return self.cachedUntil < datetime.datetime.utcnow()

class Asset(models.Model):
  assetList         = models.ForeignKey('AssetList')
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

# ============================================================================================
# = /char/WalletTransactions.xml.aspx                                                        =
# ============================================================================================

#class WalletTransaction(models.Model):
#  transactionID         = models.BigIntegerField()
#  transactionDateTime   = models.DateTimeField()
#  quantity              = models.IntegerField()
#  typeID 	             = models.ForeignKey('evedb.InvTypes')
#  price                 = models.DecimalField()
#  clientID 	           = models.ForeignKey('Characters.characterID')
#  stationID 	           =
#  transactionType 	     = models.CharField(max_length=4)
#  transactionFor        = models.CharField(max_length=11)
#  journalTransactionID  =