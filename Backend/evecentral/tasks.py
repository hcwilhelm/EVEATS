# ===========================================================================
# = Import Models and helpers                                               =
# ===========================================================================
from evedb.models import *
from common.models import TaskLastRun
from common.tasks import locktask
from helper import getXMLFromEveCentralAPI
# ===========================================================================
# = Import celery modules                                                   =
# ===========================================================================
from celery.task import Task
from celery.task import task

# ===========================================================================
# = Import general python modules                                           =
# ===========================================================================
import urllib

# ===========================================================================
# = Logging                                                                 =
# ===========================================================================
import logging
logger = logging.getLogger(__name__)

# ===================================
# = Update Character from EVE API   =
# ===================================
class UpdateAllMarketOrders(Task):
  def run(self):
    allItems = invTypes.objects.all()
    logger.info("Got %s Items from database" % allItems.count())

    for item in allItems:
      logger.info("Updating Item '%s'" % item.typeName)
      updateMarketOrder.delay(item.typeID)

    return True

@task
@locktask
def updateMarketOrder(itemTypeId):
  lastFetch, created = TaskLastRun.objects.get_or_create(taskName='updateMarketOrder', parameterValue=itemTypeId)
  now = datetime.datetime.now()

  if lastFetch.lastRun is None:
    hours = 360
  else:
    delta = now - lastFetch.lastRun
    deltaHours = int(round(delta.total_seconds() / 60, 0))
    hours = deltaHours if deltaHours > 1 else 1

  action = "/eve/CharacterInfo.xml.aspx"
  params = urllib.urlencode({'typeid': itemTypeId, 'sethours': hours})
  xml = getXMLFromEveCentralAPI(action=action, params=params)

  if xml is None:
    logging.error("Unable to fetch itemID %s from EVE Central" % itemTypeId)
  else:
    logging.info("Got data for itemID %s" % itemTypeId)

  lastFetch.lastRun = now
  lastFetch.save()

  if not created:
    logger.warning("Delete must be implemented here")

  logger.error("Not implemented")