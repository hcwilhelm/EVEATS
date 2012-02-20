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
    print "ImportAPIKeyInfoTask : " + str(key_id)
    
    apiKey = APIKey.objects.get(pk=key_id)
    
    
    # ===========================
    # = Get the XML elementTree =
    # ===========================
    
    xml_root  = self.getElementTree(apiKey)
    
    # =================================
    # = Check if the apiKey is Valid  =
    # =================================
    
    if xml_root.find("error") != None:
      apiKey.valid = False
      apiKey.save()
      
      return True
    
    else:
      apiKey.valid = True
      
    # ========================
    # = Ok the Key is Valid  =
    # ========================
    
    xml_key   = xml_root.find("result/key")
    xml_until = xml_root.find("cachedUntil")
      
    # =========================
    # = create new ApiKeyInfo =
    # =========================
    
    expires     = None
    cachedUntil = datetime.datetime.strptime(xml_until.text, "%Y-%m-%d %H:%M:%S")
    
    if xml_key.get("expires") != "":
      expires = datetime.datetime.strptime(xml_key.get("expires"), "%Y-%m-%d %H:%M:%S")
    
    apiKeyInfo = APIKeyInfo(accessMask=xml_key.get("accessMask"), 
                            accountType=xml_key.get("type"), 
                            expires=expires,
                            cachedUntil=cachedUntil)
    apiKeyInfo.save()
    
    apiKey.apiKeyInfo = apiKeyInfo
    apiKey.save()
    
    # =========================
    # = import the Characters =
    # =========================
    
    for xml_row in xml_key.find("rowset"):
      apiKey.characters_set.create(characterID=xml_row.get("characterID"), 
                                   characterName=xml_row.get("characterName"), 
                                   corporationID=xml_row.get("corporationID"), 
                                   corporationName=xml_row.get("corporationName"))
    

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
