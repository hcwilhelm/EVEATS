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
from lxml import etree
from eve.models import *
import httplib
import urllib
import datetime
from decimal import *
import logging
logger = logging.getLogger(__name__)

LOCK_EXPIRE = 60 * 5 # Lock expires in 5 minutes
# ===========================================================================
# = Celery Tasks : All model updates should be performed as a seperate task =
# ===========================================================================

class LockableTask(Task):

  def __init__(self):
    Task.__init__(self)
    self.acquireLock()

  def __del__(self):
    self.releaseLock()

  #
  # Overwrite getLockID in inherited classes
  #

  def getLockID(self):
    return 0

  def acquireLock(self):
    cache.add(self.getLockID(), "true", LOCK_EXPIRE)

  def releaseLock(self):
    cache.delete(self.getLockID())


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

class UpdateCharacter(Task):
  def run(self, character, force=False):
    returnVal = False
    if force or (character.expired and not character.isDeleted):
      lock_id = "%s-lock-%s" % (self.name, character.characterID)
      # cache.add fails if if the key already exists
      acquire_lock = lambda: cache.add(lock_id, "true", LOCK_EXPIRE)
      # memcached delete is very slow, but we have to use it to take
      # advantage of using add() for atomic locking
      release_lock = lambda: cache.delete(lock_id)

      if acquire_lock():
        try:
          keys = character.apiKeys.all()
          logger.info("Found %s API Keys for Character '%s'" % (keys.count(), character.characterName))

          action = "/eve/CharacterInfo.xml.aspx"
          params = urllib.urlencode({'characterID':character.characterID})
          xml = getXMLFromAPI(action=action, params=params)

          error = xml.find("error")
          if error is not None:
            errorCode = error.get('code')
            errorMessage = error.text

            if errorCode == "105":
              logger.warning("Marking character '%s' with id '%s' as deleted, got errorcode 105 from EVE API" %
                             (character.characterName, character.characterID))
              character.isDeleted = True
              character.save()
            elif errorCode == "522":
              logging.warning("Got errorcode 522 for characterID '%s' (Name: '%s') - setting cachedUntil +1day" %
                              (character.characterID, character.characterName))
              character.cachedUntil = datetime.datetime.utcnow() + datetime.timedelta(days=1)
              character.save()
            else:
              # unknown error
              logging.error("Got this error from EVE API: '%s' - Code '%s' - characterID '%s' - characterName '%s'" %
                            (errorMessage, errorCode, character.characterID, character.characterName))
          else:
            character.characterName = xml.find("result/characterName").text
            character.securityStatus = xml.find("result/securityStatus").text
            character.bloodline = xml.find("result/bloodline").text
            character.race = xml.find("result/race").text
            character.cachedUntil = datetime.datetime.strptime(xml.find("cachedUntil").text, "%Y-%m-%d %H:%M:%S")
            character.save()

            for employment in xml.findall("result/rowset[@name='employmentHistory']/row"):
              # first we need the corp
              corporationID = employment.get('corporationID')

              corp, created = Corporation.objects.get_or_create(corporationID=corporationID)
              if created:
                corp.save()
                UpdateCorporation.delay(corp)

              startDate = datetime.datetime.strptime(employment.get('startDate'), "%Y-%m-%d %H:%M:%S")

              newEmployment, created =  CharacterEmploymentHistory.objects.get_or_create(character=character,
                corporation=corp, startDate=startDate)
              if created:
                newEmployment.save()
            returnVal = True
        finally:
          release_lock()
      else:
        logging.warning("Unable to acquire lock to updating characterID '%s' - characterName '%s'" %
                        (character.characterID, character.characterName))
    return returnVal



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

class UpdateCharacterTask(Task):

  def run(self, char_id):
    print "UpdateCharacterTask : " + str(char_id)

    char    = Character.objects.get(pk=char_id) if Characters.objects.get(pk=char_id).exists() else Character(characterID=char_id)

    action  = "/eve/CharacterInfo.xml.aspx"
    params  = urllib.urlencode({'characterID':char_id})
    xml     = getXMLFromAPI(action, params)

    xml_current = xml.find("currentTime")
    xml_result  = xml.find("result")
    xml_rowset  = xml.find("result/rowset[@name='characters']")

    char.currentTime    = datetime.datetime.strptime(xml_current.text, "%Y-%m-%d %H:%M:%S")
    char.characterName  = xml_result.find("characterName").text
    char.race           = xml_result.find("race").text
    char.bloodline      = xml_result.find("bloodline").text
    char.securityStatus = Decimal(xml_rsult.find("securityStatus").text)


    for xml_row in xml_rowset.iter("row"):
      obj = CharacterEmploymentHistory()

      obj.character_id    = char_id
      obj.corporation_id  = xml_row.get("corporationID")
      obj.startDate       = datetime.datetime.strptime(xml_row.get("startDate"), "%Y-%m-%d %H:%M:%S")

      obj.save()

    return True

# ============================================================================
# = Class ImportAPIKeyInfoTask                                               =
# ============================================================================

class UpdateAPIKeyInfoTask(Task):

  def run(self, key_id):
    print "ImportAPIKeyInfoTask : " + str(key_id)

    apiKey  = APIKey.objects.get(pk=key_id)

    action  = "/account/APIKeyInfo.xml.aspx"
    params  = urllib.urlencode({'keyID':apiKey.keyID, 'vCode':apiKey.vCode})
    xml     = getXMLFromAPI(action, params)

    if xml.find("error") != None:
      apiKey.valid = False

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
          charAPIKeys = CharacterAPIKeys()

          charAPIKeys.apiKey_id     = key_id
          charAPIKeys.character_id  = xml_row.get("characterID")

          charAPIKeys.save()

      else:
        xml_row     = xml_rowset.find("row")
        corpAPIKeys = CorporationAPIKeys()

        corpAPIKeys.apiKey_id       = key_id
        corpAPIKeys.corporation_id  = xml_row.get("corporationID")
        corpAPIKeys.provider_id     = xml_row.get("characterID")

        corpAPIKeys.save()

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