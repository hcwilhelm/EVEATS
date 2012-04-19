#
#  tasks.py
#  Backend
#
#  Created by Hans Christian Wilhelm on 2012-02-15.
#  Copyright 2012 scienceondope.org All rights reserved.
#
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from celery.task import Task
from celery.task import task
from lxml import etree
from eve.models import *
import httplib
import urllib
import datetime
from decimal import *
import logging
import functools
logger = logging.getLogger(__name__)


# ===========================================================================
# = Decorator to allow only one update task for each object at time         =
# ===========================================================================

LOCK_EXPIRE = 60 * 5 # Lock expires in 5 minutes

def locktask(function):
  
  @functools.wraps(function)
  def wrapper(object):
    lock_id = function.__name__ + "-" + str(object.pk)
    acquire_lock = lambda: cache.add(lock_id, "true", LOCK_EXPIRE)
    release_lock = lambda: cache.delete(lock_id)

    print object
    
    if acquire_lock():
      try:
        print "Locked : " + lock_id
        function(object)
    
      finally:
        release_lock()
        print "Unlocked : " + lock_id
    
  return wrapper


# ===================================
# = Update Character from EVE API   =
# ===================================
class UpdateAllCharacters(Task):
  def run(self):

    allActiveChars = Character.objects.filter(isDeleted=False)
    logger.info("Got %s characters from database" % allActiveChars.count())

    for currentChar in allActiveChars:
      if currentChar.expired():
        logger.info("Updating character '%s'" % currentChar.characterName)
        # TODO: this must be a subtask
        UpdateCharacter.delay(currentChar)
      else:
        logger.info("Not updating character '%s'" % currentChar.characterName)

    return True

# ============================================================================
# = Class UpdateCharacter                                                    =
# ============================================================================

@task
@locktask
def updateCharacter(character):
  
  print "updateCharacter : " + str(character.pk)
  
  action = "/eve/CharacterInfo.xml.aspx"
  params = urllib.urlencode({'characterID':character.characterID})
  xml = getXMLFromAPI(action=action, params=params)

  error = xml.find("error")
  
  # ===================
  # = Error handling  =
  # ===================
  
  if error is not None:
    errorCode     = error.get('code')
    errorMessage  = error.text

    if errorCode == "105":
      logger.warning("Marking character '%s' with id '%s' as deleted, got errorcode 105 from EVE API" % (character.characterName, character.characterID))
      
      character.isDeleted = True
      character.save()
      
    elif errorCode == "522":
      logging.warning("Got errorcode 522 for characterID '%s' (Name: '%s') - setting cachedUntil +1day" % (character.characterID, character.characterName))
      
      character.cachedUntil = datetime.datetime.utcnow() + datetime.timedelta(days=1)
      character.save()
    
    else:
      logging.error("Got this error from EVE API: '%s' - Code '%s' - characterID '%s' - characterName '%s'" % (errorMessage, errorCode, character.characterID, character.characterName))
          
  # ============
  # = No error =
  # ============
  
  else:
    character.characterName     = xml.find("result/characterName").text
    character.securityStatus    = xml.find("result/securityStatus").text
    character.bloodline         = xml.find("result/bloodline").text
    character.race              = xml.find("result/race").text
    character.cachedUntil       = datetime.datetime.strptime(xml.find("cachedUntil").text, "%Y-%m-%d %H:%M:%S")
    
    character.save()

    for employment in xml.findall("result/rowset[@name='employmentHistory']/row"):
      
      corp, created = Corporation.objects.get_or_create(corporationID=employment.get('corporationID'))
      
      #
      # If created we could start an Corporation update job.
      # Anyways a new created character is always expired so it will be update
      # by the next query.
      #
      
      startDate = datetime.datetime.strptime(employment.get('startDate'), "%Y-%m-%d %H:%M:%S")

      CharacterEmploymentHistory.objects.get_or_create(character=character, corporation=corp, startDate=startDate)
  
  # ================
  # = Update done  =
  # ================
  
  return True



class UpdateCorporation(Task):
  def run(self, corporation, force=False):
    if force or corporation.expired():
      action = "/corp/CorporationSheet.xml.aspx"
      params = urllib.urlencode({'corporationID':corporation.corporationID})
      xml = getXMLFromAPI(action=action, params=params)

      if xml.find("error") is not None:
        return False
      else:
        corporation.corporationName = xml.find("result/corporationName").text
        corporation.description = xml.find("result/description").text

        ceo, created = Character.objects.get_or_create(characterID = xml.find("result/ceoID").text)
        if created:
          # we will store the ceo name here for noob corps, those chars are not
          # fetchable via api so we can't get the name during the update later
          # and storing chars without names would be very ugly!
          ceo.characterName = xml.find("result/ceoName").text
          ceo.save()
          logger.info("Created character with id %s" % ceo.characterID)
          UpdateCharacter.delay(ceo)

        corporation.ceo = ceo
        corporation.cachedUntil = datetime.datetime.strptime(xml.find("cachedUntil").text, "%Y-%m-%d %H:%M:%S")
        corporation.save()

        return True


# ============================================================================
# = Class UpdateCharacter                                                    =
# ============================================================================


# ============================================================================
# = updateAPIKey                                                             =
# ============================================================================

@task
@locktask
def updateAPIKey(apiKey):
  print "ImportAPIKeyInfoTask : " + str(apiKey.id)

  action  = "/account/APIKeyInfo.xml.aspx"
  params  = urllib.urlencode({'keyID':apiKey.keyID, 'vCode':apiKey.vCode})
  xml     = getXMLFromAPI(action, params)

  if xml.find("error") != None:
    apiKey.valid        = False
    apiKey.cachedUntil  = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)

  else:
    xml_current = xml.find("currentTime")
    xml_key     = xml.find("result/key")
    xml_rowset  = xml.find("result/key/rowset")
    xml_until   = xml.find("cachedUntil")

    apiKey.valid        = True
    apiKey.currentTime  = datetime.datetime.strptime(xml_current.text, "%Y-%m-%d %H:%M:%S")
    apiKey.accessMask   = xml_key.get("accessMask")
    apiKey.accountType  = xml_key.get("type")
    apiKey.expires      = None if xml_key.get("expires") == "" else datetime.datetime.strptime(xml_key.get("expires"), "%Y-%m-%d %H:%M:%S")
    apiKey.cachedUntil  = datetime.datetime.strptime(xml_until.text, "%Y-%m-%d %H:%M:%S")

    apiKey.save()

    if apiKey.accountType == "Account":
      for xml_row in xml_rowset.iter("row"):
        
        character, created = Character.objects.get_or_create(pk=xml_row.get("characterID"))
        
        if created:
          updateCharacter.delay(character)
          
        #
        # If created we could start an character update job.
        # Anyways a new created character is always expired so it will be update
        # by the next query.
        #
        
        CharacterAPIKeys.objects.get_or_create(apiKey=apiKey, character=character)

    else:
      for xml_row in xml_rowset.iter("row"):
        
        character, created = Character.objects.get_ort_create(pk=xml_row.get("characterID"))
        
        #
        # If created we could start an character update job.
        # Anyways a new created character is always expired so it will be update
        # by the next query.
        #
        
        corporation, created = Corporation.objects.get_or_create(pk=xml_row.get("corporationID"))
        
        #
        # If created we could start an corporation update job.
        # Anyways a new created character is always expired so it will be update
        # by the next query.
        #
        
        CorporationAPIKeys.objects.get_or_create(apiKey=apiKey, corporation=corporation, provider=character)

  return True

# ============================================================================
# = Class ImportAssetListTask                                                =
# ============================================================================

class UpdateAssetListTask(Task):

  def run(self, char_id):

    print "ImportAssetListTask : " + str(char_id)

    character = Characters.objects.get(pk=char_id)

    # ============
    # = clean up =
    # ============

    character.assetlist_set.all().delete()

    # ===========================
    # = Get the XML elementTree =
    # ===========================

    xml_root  = self.getElementTree(character)

    # ===================
    # = Check for Error =
    # ===================

    if xml_root.find("error") != None:
      return False

    # =============
    # = No Error  =
    # =============

    else:

      xml_assets  = xml_root.find("result/rowset")
      xml_current = xml_root.find("currentTime")
      xml_until   = xml_root.find("cachedUntil")

      currentTime = datetime.datetime.strptime(xml_current.text, "%Y-%m-%d %H:%M:%S")
      cachedUntil = datetime.datetime.strptime(xml_until.text, "%Y-%m-%d %H:%M:%S")

      assetList = AssetList(character=character, currentTime=currentTime, cachedUntil=cachedUntil)
      assetList.save()

      stack   = [None]
      parent  = None
      context = etree.iterwalk(xml_assets, events=("start", "end"))

      total = xml_assets.xpath('count(//row)')
      current = 0

      for action, element in context:
        if element.tag == "rowset":

          if element.get("name") == "assets":
            continue

          if action == "start" and element.get("name") == "contents":
            stack.append(parent)

          if action == "end" and element.get("name") == "contents":
            stack.pop()

        if element.tag == "row" and action == "start":
          asset             = Assets()
          asset.assetList   = assetList
          asset.parent      = stack[-1]
          asset.itemID      = element.get("itemID")

          if element.get("locationID") != None:

            # ==========================================================================
            # = officeID to stationID conversion refer to eve dev for more information =
            # ==========================================================================

            locationID = element.get("locationID")

            if locationID >= 66000000 and locationID < 67000000:
                locationID -= 6000001

            asset.locationID_id  = locationID

          asset.typeID_id   = element.get("typeID")
          asset.quantity    = element.get("quantity")
          asset.flag_id     = element.get("flag")
          asset.singleton   = element.get("singleton")
          rawQuantity       = element.get("rawQuantity")

          asset.save()
          parent = asset

          current += 1
          UpdateAssetListTask.update_state(self, state="PROGRESS", meta={"current": current, "total": int(total)})

      print "ImportAssetListTask : " + str(char_id) + " : Done"
      return True

  def getElementTree(self, char):

    action = ""

    if char.apiKeyInfo.accountType == "Account":
      action = "/char/AssetList.xml.aspx"

    if char.apiKeyInfo.accountType == "Corporation":
      action = "/corp/AssetList.xml.aspx"

    key = APIKey.objects.get(apiKeyInfo=char.apiKeyInfo)

    params = urllib.urlencode({'keyID':key.keyID, 'vCode':key.vCode, 'characterID':char.characterID})
    header = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

    connection = httplib.HTTPSConnection(settings.EVE_API_HOST, settings.EVE_API_PORT)
    connection.request("GET", action, params, header)

    xml = connection.getresponse().read()
    connection.close()

    return etree.fromstring(xml)



def getXMLFromAPI(action, params):
    header = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

    connection = httplib.HTTPSConnection(settings.EVE_API_HOST, settings.EVE_API_PORT)
    connection.request("GET", action, params, header)

    xml = connection.getresponse().read()
    connection.close()
    return etree.fromstring(xml)