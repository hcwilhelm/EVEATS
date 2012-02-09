#  models.py
#  EVEARS
#  
#  Created by Hans Christian Wilhelm on 2011-09-05.
#  Copyright 2011 scienceondope.org All rights reserved.
# 

from django.db import models
from django.contrib.auth.models import User

import xml.etree.ElementTree as ElementTree
import httplib
import urllib

baseURL = "api.eveonline.com"
header  = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

class APIKey(models.Model):
  keyID           = models.IntegerField(null=False)
  vCode           = models.CharField(max_length=64, null=False)
  name            = models.CharField(max_length=128)
  user            = models.ForeignKey(User)

class APIKeyInfo(models.Model):
  apiKey          = models.ForeignKey(APIKey)
  accessMask      = models.IntegerField()
  type            = models.CharField(max_length=64)
  expires         = models.DateField()
  chachedUntil    = models.DateField()
  
  @staticmethod
  def update(apiKeyObject):
    params   = urllib.urlencode({'keyID' : apiKeyObject.keyID, 'vCode' : apiKeyObject.vCode})
    
    connection  = httplib.HTTPSConnection(baseURL, 443)
    connection.request("GET", "/account/APIKeyInfo.xml.aspx", params, header)
    
    data = connection.getresponse().read()
    print data
    connection.close()
    
    xmlTree = ElementTree.fromstring(data)
    print xmlTree
    

class APIKeyInfoRowset(models.Model):
  apiKeyInfo        = models.ForeignKey(APIKeyInfo)
  characterID       = models.IntegerField()
  characterName     = models.CharField(max_length=128)
  corporationID     = models.IntegerField()
  corporationName   = models.CharField(max_length=128)

