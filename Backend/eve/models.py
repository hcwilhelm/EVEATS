#  models.py
#  EVEATS
#
#  Created by Hans Christian Wilhelm on 2011-09-05.
#  Copyright 2011 scienceondope.org All rights reserved.

from django.db import models

from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from django.core.exceptions import ValidationError

from evedb.models import *

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
  allianceName      = models.CharField(max_length=255, null=True)

class Corporation(models.Model):
  corporationID     = models.IntegerField(primary_key=True)
  corporationName   = models.CharField(max_length=255, null=True)
  ceo               = models.ForeignKey('Character', null=True)
  description       = models.TextField(null=True)
  cachedUntil       = models.DateTimeField(default=datetime.datetime.utcnow(), blank=True)
  alliances         = models.ManyToManyField('Alliance', through='CorporationAllianceHistory', null=True)
  apiKeys           = models.ManyToManyField('APIKey', through='CorporationAPIKeys', null=True)
  isDeleted         = models.BooleanField(default=False)
  assetList         = models.ForeignKey('AssetList', null=True, on_delete=models.SET_NULL)

  def expired(self):
    return self.cachedUntil < datetime.datetime.utcnow()

  class Meta:
    permissions = (
      ("viewAssetList_corporation", "Can see available assetList"),
    )

class Character(models.Model):
  characterID       = models.IntegerField(primary_key=True)
  characterName     = models.CharField(max_length=255, null=True)
  securityStatus    = models.DecimalField(decimal_places=16, max_digits=18, null=True)
  race              = models.CharField(max_length=64, null=True)
  bloodline         = models.CharField(max_length=64, null=True)
  isDeleted         = models.BooleanField(default=False)
  cachedUntil       = models.DateTimeField(default=datetime.datetime.utcnow(), blank=True)
  corporations      = models.ManyToManyField('Corporation', through='CharacterEmploymentHistory', null=True)
  apiKeys           = models.ManyToManyField('APIKey', through='CharacterAPIKeys', null=True)
  assetList         = models.ForeignKey('AssetList', null=True, on_delete=models.SET_NULL)

  def expired(self):
    return self.cachedUntil < datetime.datetime.utcnow()

  class Meta:
    permissions = (
      ("viewAssetList_character", "Can see available assetList"),
    )

class CharacterEmploymentHistory(TimeStampedModel):
  character         = models.ForeignKey('Character')
  corporation       = models.ForeignKey('Corporation')
  startDate         = models.DateTimeField()

class CorporationAllianceHistory(TimeStampedModel):
  corporation       = models.ForeignKey('Corporation')
  alliance          = models.ForeignKey('Alliance')
  startDate         = models.DateTimeField()

class AssetList(TimeStampedModel):
  currentTime       = models.DateTimeField()
  cachedUntil       = models.DateTimeField()

  def expired(self):
     return self.cachedUntil < datetime.datetime.utcnow()


#
# Polymorpic Station model to represent ether a ConquerableStation or a NPC Station.
# Allowed Types are ConquerableStation and evedb.staStations
#

def validate_station_type(obj):
  if ContentType.objects.get(pk=obj).model_class() != ConquerableStation or ContentType.objects.get(pk=obj) != staStations:
    raise ValidationError("We only link ConquerableStation and evedb.staStations here !")


#
# When you create a Station call stationObj.full_clean()
# to validate the content_type !
#

class Station(models.Model):
  content_type      = models.ForeignKey(ContentType, validators=[validate_station_type])
  object_id         = models.PositiveIntegerField()
  concreteStation   = generic.GenericForeignKey('content_type', 'object_id')
  
  def __unicode__(self):
    return str(self.concreteStation.pk)
  

class ConquerableStation(models.Model):
  stationID         = models.PositiveIntegerField(primary_key=True)
  stationName       = models.CharField(max_length=256)
  stationType       = models.ForeignKey('evedb.staStationTypes')
  solarSystem       = models.ForeignKey('evedb.mapSolarSystems')
  corporation       = models.ForeignKey('Corporation')
  cachedUntil       = models.DateTimeField(default=datetime.datetime.utcnow(), blank=True)

  def __unicode__(self):
    return self.concreteStation.stationName
    
  def expired(self):
    return self.cachedUntil < datetime.datetime.utcnow()

# =============================================================================================
# = /char/AssetList.xml.aspx                                                                  =
# =============================================================================================

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
# = Class APIKey. Note !                                                                     =
# ============================================================================================

class APIKey(models.Model):
  keyID           = models.IntegerField(null=False)
  vCode           = models.CharField(max_length=64, null=False)
  name            = models.CharField(max_length=128)
  user            = models.ForeignKey(User)
  currentTime     = models.DateTimeField(default=datetime.datetime.utcnow(), blank=True)
  accessMask      = models.IntegerField(null=True)
  accountType     = models.CharField(max_length=255, null=True)
  expires         = models.DateTimeField(null=True)
  cachedUntil     = models.DateTimeField(default=datetime.datetime.utcnow(), blank=True)
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