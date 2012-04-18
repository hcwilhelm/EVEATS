#  models.py
#  EVEATS
#
#  Created by Hans Christian Wilhelm on 2011-09-05.
#  Copyright 2011 scienceondope.org All rights reserved.

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User
import datetime
import logging
logger = logging.getLogger(__name__)

# =============================================================================================
# = Models to map API keys to chars and crops                                                 =
# =============================================================================================

class CharacterAPIKeys(TimeStampedModel):
  apiKey            = models.ForeignKey('APIKey')
  character         = models.ForeignKey('Character')

class CorporationAPIKeys(TimeStampedModel):
  apiKey            = models.ForeignKey('APIKey')
  corporation       = models.ForeignKey('Corporation')
  provider          = models.ForeignKey('Character')

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
  apiKeys           = models.ManyToManyField('APIKey', through='CorporationAPIKeys')
  isDeleted         = models.BigIntegerField(default=False)
  assets = models.ManyToManyField('Asset', through='AssetListCorporation', null=True)

  def expired(self):
    return self.cachedUntil < datetime.datetime.utcnow()

class Character(models.Model):
  characterID       = models.IntegerField(primary_key=True)
  characterName     = models.CharField(max_length=255)
  securityStatus    = models.DecimalField(decimal_places=16, max_digits=18, null=True)
  race              = models.CharField(max_length=64, null=True)
  bloodline         = models.CharField(max_length=64, null=True)
  isDeleted         = models.BooleanField(default=False)
  cachedUntil       = models.DateTimeField(default=datetime.datetime.utcnow(), blank=True)
  corporations      = models.ManyToManyField('Corporation', through='CharacterEmploymentHistory')
  apiKeys           = models.ManyToManyField('APIKey', through='CharacterAPIKeys', null=True)
  assets            = models.ManyToManyField('Asset', through='AssetListCharacter', null=True)

  def expired(self):
    return self.cachedUntil < datetime.datetime.utcnow()

class CharacterEmploymentHistory(TimeStampedModel):
  character         = models.ForeignKey('Character')
  corporation       = models.ForeignKey('Corporation')
  startDate         = models.DateTimeField()

class CorporationAllianceHistory(TimeStampedModel):
  corporation       = models.ForeignKey('Corporation')
  alliance          = models.ForeignKey('Alliance')
  startDate         = models.DateTimeField()

class AssetListCharacter(TimeStampedModel):
  character         = models.ForeignKey('Character')
  asset             = models.ForeignKey('Asset')
  currentTime       = models.DateTimeField()
  cachedUntil       = models.DateTimeField()

  def expired(self):
     return self.cachedUntil < datetime.datetime.utcnow()

class AssetListCorporation(TimeStampedModel):
  corporation = models.ForeignKey('Corporation')
  asset       = models.ForeignKey('Asset')
  currentTime = models.DateTimeField()
  cachedUntil = models.DateTimeField()

  def expired(self):
    return self.cachedUntil < datetime.datetime.utcnow()

# =============================================================================================
# = /char/AssetList.xml.aspx                                                                  =
# =============================================================================================

class Asset(models.Model):
  parent            = models.ForeignKey('self', null=True, blank=True)
  itemID            = models.BigIntegerField()
  locationID        = models.ForeignKey('evedb.mapDenormalize', null=True, blank=True)
  typeID            = models.ForeignKey('evedb.invTypes')
  quantity          = models.IntegerField()
  flag              = models.ForeignKey('evedb.invFlags')
  singleton         = models.BooleanField()
  rawQuantity       = models.IntegerField(null=True, blank=True)

# ============================================================================================
# = Class APIKey. Note !       =
# ============================================================================================

class APIKey(models.Model):
  keyID           = models.IntegerField(null=False)
  vCode           = models.CharField(max_length=64, null=False)
  name            = models.CharField(max_length=128)
  user            = models.ForeignKey(User)
  currentTime     = models.DateTimeField()
  accessMask      = models.IntegerField(null=True)
  accountType     = models.CharField(max_length=255, null=True)
  expires         = models.DateTimeField(null=True)
  cachedUntil     = models.DateTimeField()
  valid           = models.BooleanField(default=True)

  def expired(self):
    return self.cachedUntil < datetime.datetime.utcnow()

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