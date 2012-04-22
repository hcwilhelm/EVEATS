# ===========================================================================
# = Import general python modules                                           =
# ===========================================================================
from functools import wraps

# ===========================================================================
# = Import django modules                                                   =
# ===========================================================================
from django.core.cache import cache
from django.conf import settings

# ===========================================================================
# = Logging                                                                 =
# ===========================================================================
import logging
logger = logging.getLogger(__name__)

# ===========================================================================
# = Import general python modules                                           =
# ===========================================================================
from lxml import etree
import httplib

# ===========================================================================
# = Decorator to allow only one update task for each object at time         =
# ===========================================================================

LOCK_EXPIRE = 60 * 5        # Lock expires after 5 minutes
def locktask(function):
  @wraps(function)
  def wrapper(object, *args, **kwargs):
    lock_id = function.__name__ + "-" + str(object)
    acquire_lock = lambda: cache.add(lock_id, "true", LOCK_EXPIRE)
    release_lock = lambda: cache.delete(lock_id)

    if acquire_lock():
      try:
        logger.debug("Locked task: %s" % lock_id)
        return function(object, *args, **kwargs)
      except Exception as ex:
        # TODO: write more details to a file
        logger.error("Exception in Task: %s" % ex)
      finally:
        release_lock()
        logger.debug("Unlocked task: %s" % lock_id)

  return wrapper

# =============================================================================
# = Helper functions                                                          =
# =============================================================================

def getXMLFromEveAPI(action, params):
  header = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

  connection = httplib.HTTPSConnection(settings.EVE_API_HOST, settings.EVE_API_PORT)
  connection.request("GET", action, params, header)

  xml = connection.getresponse().read()
  connection.close()
  return etree.fromstring(xml)