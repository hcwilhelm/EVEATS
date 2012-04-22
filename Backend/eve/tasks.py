# ===========================================================================
# = Import Models and helper                                                =
# ===========================================================================
from eve.models import *
from evedb.models import *
from common.tasks import getXMLFromEveAPI

# ===========================================================================
# = Import celery modules                                                   =
# ===========================================================================
from celery.task import Task
from celery.task import task

# ===========================================================================
# = Import general python modules                                           =
# ===========================================================================
from lxml import etree
import httplib
import urllib
from common.tasks import locktask

# ===========================================================================
# = Logging                                                                 =
# ===========================================================================
import logging
logger = logging.getLogger(__name__)

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
        updateCharacter.delay(currentChar.pk)
      else:
        logger.info("Not updating character '%s'" % currentChar.characterName)

    return True

# ===================================
# = Update Conquerable Stations     =
# ===================================
class UpdateConquerableStationList(Task):
  def run(self):
    action = "/eve/ConquerableStationList.xml.aspx"
    xml = getXMLFromEveAPI(action=action, params=None)

    # ===================
    # = Error handling  =
    # ===================
    error = xml.find("error")
    if error is not None:
      errorCode = error.get('code')
      errorMessage = error.text
      logger.warning("Error fetching ConquerableStationList from API: errorCode: '%s' errorMessage '%s'" % (
        errorCode, errorMessage))
      return False

    cachedUntil = datetime.datetime.strptime(xml.find("cachedUntil").text, "%Y-%m-%d %H:%M:%S")
    for outpost in xml.findall("result/rowset[@name='outposts']/row"):
      station, created = ConquerableStation.objects.get_or_create(stationID=outpost.get('stationID'))

      station.stationName = outpost.get('stationName')
      station.stationTypeID = staStationTypes.objects.get(stationTypeID=outpost.get('stationTypeID'))
      station.solarSystemID = mapSolarSystems.objects.get(solarSystemID=outpost.get('solarSystemID'))

      corporation, corpCreated = Corporation.objects.get_or_create(corporationID=outpost.get('corporationID'))

      if corpCreated:
        corporation.save()
        updateCorporation(corporation.pk)

      station.corporationID = corporation
      station.cachedUntil = cachedUntil

      station.save()

    toDelete = ConquerableStation.objects.get(cachedUntil < cachedUntil)
    logger.info("Deleting '%s' outdated conquerable Stations" % toDelete.count())
    toDelete.delete()

    return True
# ============================================================================
# = task updateCharacter                                                     =
# ============================================================================

@task
@locktask
def updateCharacter(character_id):
  logger.debug("running updateCharacter for characterId %s" % character_id)

  character = Character.objects.get(pk=character_id)

  action = "/eve/CharacterInfo.xml.aspx"
  params = urllib.urlencode({'characterID':character.characterID})
  xml = getXMLFromEveAPI(action=action, params=params)

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

      if created:
        updateCorporation(corp.pk)

      startDate = datetime.datetime.strptime(employment.get('startDate'), "%Y-%m-%d %H:%M:%S")

      CharacterEmploymentHistory.objects.get_or_create(character=character, corporation=corp, startDate=startDate)

  # ================
  # = Update done  =
  # ================

  return True

# ============================================================================
# = task updateCorporation                                                   =
# ============================================================================

@task
@locktask
def updateCorporation(corporation_id):
  logger.debug("running updateCorporation for corporationId %s" % corporation_id)

  corporation = Corporation.objects.get(pk=corporation_id)

  action = "/corp/CorporationSheet.xml.aspx"
  params = urllib.urlencode({'corporationID':corporation.corporationID})
  xml = getXMLFromEveAPI(action=action, params=params)

  # ===================
  # = Error Handling  =
  # ===================

  if xml.find("error") is not None:
    return False

  # =============
  # = No Error  =
  # =============

  else:
    corporation.corporationName = xml.find("result/corporationName").text
    corporation.description     = xml.find("result/description").text

    ceo, created = Character.objects.get_or_create(characterID=xml.find("result/ceoID").text)

    if created:

      # we will store the ceo name here for noob corps, those chars are not
      # fetchable via api so we can't get the name during the update later
      # and storing chars without names would be very ugly!

      #
      # NPC characterID's can be identified via the static data dump !
      #

      logger.info("Created character with id %s" % ceo.characterID)
      updateCharacter.delay(ceo.pk)

    corporation.ceo         = ceo
    corporation.cachedUntil = datetime.datetime.strptime(xml.find("cachedUntil").text, "%Y-%m-%d %H:%M:%S")
    corporation.save()

  # ================
  # = Update done  =
  # ================

  return True


# ============================================================================
# = Class UpdateCharacter                                                    =
# ============================================================================


# ============================================================================
# = updateAPIKey                                                             =
# ============================================================================

@task
@locktask
def updateAPIKey(apiKey_id):
  print "ImportAPIKeyInfoTask : " + str(apiKey_id)

  apiKey  = APIKey.objects.get(pk=apiKey_id)

  action  = "/account/APIKeyInfo.xml.aspx"
  params  = urllib.urlencode({'keyID':apiKey.keyID, 'vCode':apiKey.vCode})
  xml     = getXMLFromEveAPI(action, params)

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
          updateCharacter.delay(character.pk)

        #
        # If created we could start an character update job.
        # Anyways a new created character is always expired so it will be update
        # by the next query.
        #

        CharacterAPIKeys.objects.get_or_create(apiKey=apiKey, character=character)

    else:
      for xml_row in xml_rowset.iter("row"):

        character, created = Character.objects.get_or_create(pk=xml_row.get("characterID"))

        if created:
          updateCharacter.delay(character.pk)

        #
        # If created we could start an character update job.
        # Anyways a new created character is always expired so it will be update
        # by the next query.
        #

        corporation, created = Corporation.objects.get_or_create(pk=xml_row.get("corporationID"))

        if created:
          updateCorporation(corporation.pk)

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


#
# this Taks excepts Character or Corporation objects !!!
# Maybe it is useful to extend this to APIKey objects also, dunno
#

@task
@locktask
def updateAssetList(object_id, type):

    print "ImportAssetListTask : " + str(object_id)

    object    = None
    xml_root  = None

    #
    # Check if the object is a Character
    #

    if type == Character:

      object = Character.objects.get(pk=object_id)

      #
      # Check if the object has a related APIKey
      #

      if not object.apiKeys.all().exists():
        return False

      apiKey  = object.apiKeys.all()[0]
      char    = object
      action  = "/char/AssetList.xml.aspx"
      params  = urllib.urlencode({'keyID':apiKey.keyID, 'vCode':apiKey.vCode, 'characterID':char.characterID})

      xml_root     = getXMLFromEveAPI(action, params)

    #
    # Check if the object is a Corporation
    #

    elif type == Corporation:

      object = Corporation.objects.get(pk=object_id)

      #
      # Check if the object has a related APIKey
      #

      if not object.apiKeys.all().exists():
        return False

      apiKey  = object.apiKeys.all()[0]
      char    = CorporationAPIKeys.objects.get(apiKey=apiKey, corporation=object).provider
      action  = "/corp/AssetList.xml.aspx"
      params  = urllib.urlencode({'keyID':apiKey.keyID, 'vCode':apiKey.vCode, 'characterID':char.characterID})

      xml_root     = getXMLFromEveAPI(action, params)

    #
    # Do nothing for all other object types
    #

    else:
      return False

    #
    # Clean up older assets
    #

    if object.assetList != None:
      object.assetList.asset_set.all().delete()

    #
    # Error Handling
    #

    if xml_root.find("error") != None:
      print xml_root.find("error").text
      return False

    #
    # No Error
    #

    xml_assets  = xml_root.find("result/rowset")
    xml_current = xml_root.find("currentTime")
    xml_until   = xml_root.find("cachedUntil")

    currentTime = datetime.datetime.strptime(xml_current.text, "%Y-%m-%d %H:%M:%S")
    cachedUntil = datetime.datetime.strptime(xml_until.text, "%Y-%m-%d %H:%M:%S")

    assetList = AssetList(currentTime=currentTime, cachedUntil=cachedUntil)
    assetList.save()

    object.assetList = assetList
    object.save()

    stack   = [None]
    parent  = None
    context = etree.iterwalk(xml_assets, events=("start", "end"))

    total   = xml_assets.xpath('count(//row)')
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
        asset             = Asset()
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

        #
        # Custom state to expose progress to the Frontend ;)
        #

        updateAssetList.update_state(state="PROGRESS", meta={"current": current, "total": int(total)})

    print "ImportAssetListTask : " + str(object.pk) + " : Done"
    return True





