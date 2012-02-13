#  models.py
#  EVEARS
#  
#  Created by Hans Christian Wilhelm on 2011-09-05.
#  Copyright 2011 scienceondope.org All rights reserved.
# 

from django.db import models
from django.contrib.auth.models import User

from Backend.eveapi.client import EVEError 
from Backend.eveapi.client import EVEClient

import datetime

# ============================================================================================
# = APIKeyInfo and associated rows. See  http://wiki.eve-id.net/APIv2_Account_APIKeyInfo_XML =
# ============================================================================================

class APIKeyInfo(models.Model):
  accessMask      = models.IntegerField()
  type            = models.CharField(max_length=64)
  expires         = models.DateTimeField(null=True)
  chachedUntil    = models.DateTimeField()
  
  def expired(self):
    return self.chachedUntil < datetime.datetime.utcnow()

class APIKeyInfoRow(models.Model):
  apiKeyInfo        = models.ForeignKey(APIKeyInfo)
  characterID       = models.IntegerField()
  characterName     = models.CharField(max_length=128)
  corporationID     = models.IntegerField()
  corporationName   = models.CharField(max_length=128)

# ======================================================================================
# = Class APIKey. Note ! Stricly use costum get methods to acces related model objects =
# ======================================================================================

class APIKey(models.Model):
  keyID           = models.IntegerField(null=False)
  vCode           = models.CharField(max_length=64, null=False)
  name            = models.CharField(max_length=128)
  user            = models.ForeignKey(User)
  apiKeyInfo      = models.ForeignKey(APIKeyInfo, null=True)
  
  def getAPIKeyInfo(self):
    if apiKeyInfo == None:
      client = EVEClient(self)
      
      xml   = client.getAPIKeyInfo()
      key   = xml.find("result/key")
      until = xml.find("cachedUntil") 
      
      apiKeyInfo              = APIKeyInfo();
      apiKeyInfo.accessMask   = key.attrib['accessMask']
      apiKeyInfo.type         = key.attrib['type']
      apiKeyInfo.chachedUntil = datetime.datetime.strptime(until.text, "%Y-%m-%d %H:%M:%S")
      
      if key.attrib['expires'] != "":
        apiKeyInfo.expires    = datetime.datetime.strptime(key.attrib['expires'], "%Y-%m-%d %H:%M:%S")
      
      apiKeyInfo.save()
      
      for row in key.find("rowset").getchildren():
        apiKeyInfoRow                 = APIKeyInfoRow()
        apiKeyInfoRow.apiKeyInfo      = apiKeyInfo
        apiKeyInfoRow.characterID     = row.attrib['characterID']
        apiKeyInfoRow.characterName   = row.attrib['characterName']
        apiKeyInfoRow.corporationID   = row.attrib['corporationID']
        apiKeyInfoRow.corporationName = row.attrib['corporationName']
        apiKeyInfoRow.save()
        
    else if self.apiKeyInfo.expired():
      
      



