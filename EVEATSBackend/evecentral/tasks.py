# ===========================================================================
# = Import Models and helpers                                               =
# ===========================================================================
from evedb.models import *
from common.models import TaskLastRun
from common.tasks import locktask
from helper import getXMLFromEveCentralAPI

# ===========================================================================
# = Import celery modules =
# ===========================================================================
from celery import Task
from celery import task

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

    action = "/api/quicklook"
    params = urllib.urlencode({'typeid': itemTypeId, 'sethours': hours, 'setminQ': 1})
    xml = getXMLFromEveCentralAPI(action=action, params=params)

    error = xml.find("error")
    if error is not None:
        errorMessage  = error.text
        logger.warning("Error fetching marketOrders from EVE Central API: '%s'" % (errorMessage))
        return False
    
    sellOrders = xml.findall("evec_api/quicklook/sell_orders/order")
    logger.info("Fetched %s selling orders from EVE Central" % len(sellOrders))
    buyOrders = xml.findall("evec_api/quicklook/buy_orders/order")
    logger.info("Fetched %s buying orders from EVE Central" % len(buyOrders))    
    
    lastFetch.lastRun = now
    lastFetch.save()