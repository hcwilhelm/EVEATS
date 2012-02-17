# 
#  tasks.py
#  Backend
#  
#  Created by Hans Christian Wilhelm on 2012-02-15.
#  Copyright 2012 scienceondope.org All rights reserved.
# 


# ===========================================================================
# = Celery Tasks : All model updates should be performed as a seperate task =
# ===========================================================================

from django.conf import settings
from celery.task import Task
from lxml import etree

from eveapi.models import APIKey
from eveapi.models import APIKeyInfo
from eveapi.models import Characters

import httplib
import urllib
import datetime
import time

# ============================================================================
# = Class ImportAPIKeyInfoTask                                               =
# ============================================================================
class ImportAPIKeyInfoTask(Task):
  
  def run(self, key_id):
    print "ImportAPIKeyInfoTask"
    
    apiKey = APIKey.objects.get(pk=key_id)
    
    if apiKey.apiKeyInfo == None:
      
      # =====================
      # = Find the xml tags =
      # =====================
      
      xml_root  = self.getElementTree(apiKey)
      xml_key   = xml_root.find("result/key")
      xml_until = xml_root.find("cachedUntil")
      
      # =========================
      # = create new ApiKeyInfo =
      # =========================
      
      expires     = None
      cachedUntil = datetime.datetime.strptime(xml_until.text, "%Y-%m-%d %H:%M:%S")
      
      if xml_key.get("expires") != "":
        expires = datetime.datetime.strptime(xml_key.get("expires"), "%Y-%m-%d %H:%M:%S")
      
      apiKeyInfo = APIKeyInfo(accessMask=xml_key.get("accessMask"), accountType=xml_key.get("type"), expires=expires, cachedUntil=cachedUntil)
      apiKeyInfo.save()
      
      apiKey.apiKeyInfo = apiKeyInfo
      apiKey.save()
      
      # ===========================
      # = Use the Character list  =
      # ===========================
      
      apiKey.characters_set.all().delete()
      
      for xml_row in xml_key.find("rowset"):
        apiKey.characters_set.create(characterID=xml_row.get("characterID"), 
                                    characterName=xml_row.get("characterName"), 
                                    corporationID=xml_row.get("corporationID"), 
                                    corporationName=xml_row.get("corporationName"), 
                                    cachedUntil=cachedUntil)
      
    elif apiKey.apiKeyInfo.expired():

      # =====================
      # = Find the xml tags =
      # =====================

      xml_root  = self.getElementTree(apiKey)
      xml_key   = xml_root.find("result/key")
      xml_until = xml_root.find("cachedUntil")

      # =========================
      # = update ApiKeyInfo =
      # =========================

      expires     = None
      cachedUntil = datetime.datetime.strptime(xml_until.text, "%Y-%m-%d %H:%M:%S")

      if xml_key.get("expires") != "":
        expires = datetime.datetime.strptime(xml_key.get("expires"), "%Y-%m-%d %H:%M:%S")

      apiKeyInfo              = apiKey.apiKeyInfo
      apiKeyInfo.accessMask   = xml_key.get("accessMask")
      apiKeyInfo.accountType  = xml_key.get("type")
      apiKeyInfo.expires      = expires
      apiKeyInfo.cachedUntil  = cachedUntil
      apiKeyInfo.save()

      # ===========================
      # = Use the Character list  =
      # ===========================

      apiKey.characters_set.all().delete()

      for xml_row in xml_key.find("rowset"):
        apiKey.characters_set.create(characterID=xml_row.get("characterID"), 
                                    characterName=xml_row.get("characterName"), 
                                    corporationID=xml_row.get("corporationID"), 
                                    corporationName=xml_row.get("corporationName"), 
                                    cachedUntil=cachedUntil)

    return True

  def getElementTree(self, key):

    action = "/account/APIKeyInfo.xml.aspx"
    params = urllib.urlencode({'keyID':key.keyID, 'vCode':key.vCode})
    header = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

    connection = httplib.HTTPSConnection(settings.EVE_API_HOST, settings.EVE_API_PORT)
    connection.request("GET", action, params, header)

    xml = connection.getresponse().read()
    connection.close()

    return etree.fromstring(xml)

# ============================================================================================
# = Class ImportCharactersTask                                                               =
# ============================================================================================

class ImportCharactersTask(Task):
  
  def run(self, apiKey_id):
    print "ImportCharactersTask"
    
    apiKey      = APIKey.objects.get(pk=apiKey_id)
    needsUpdate = False
    
    # =============================
    # = test if something expired =
    # =============================
    
    for char in apiKey.characters_set.all():
      if char.expired():
        needsUpdate = True;
        break
    
    if len(apiKey.characters_set.all()) == 0:
      needsUpdate = True;
    
    # ===========================
    # = Use the Character list  =
    # ===========================
    
    if needsUpdate:
      xml_root  = self.getElementTree(apiKey)
      xml_until = xml_root.find("cachedUntil")
      
      apiKey.characters_set.all().delete()
      
      for xml_row in xml_root.find("result/rowset"):
        apiKey.characters_set.create(characterID=xml_row.get("characterID"), 
                                    characterName=xml_row.get("name"), 
                                    corporationID=xml_row.get("corporationID"), 
                                    corporationName=xml_row.get("corporationName"), 
                                    cachedUntil=datetime.datetime.strptime(xml_until.text, ("%Y-%m-%d %H:%M:%S")))
                                    
    return True
    
  def getElementTree(self, key):
    
    action = "/account/Characters.xml.aspx"
    params = urllib.urlencode({'keyID':key.keyID, 'vCode':key.vCode})
    header = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

    connection = httplib.HTTPSConnection(settings.EVE_API_HOST, settings.EVE_API_PORT)
    connection.request("GET", action, params, header)

    xml = connection.getresponse().read()
    connection.close()

    return etree.fromstring(xml)