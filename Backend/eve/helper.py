# ===========================================================================
# = Import django modules                                                   =
# ===========================================================================
from django.conf import settings

# ===========================================================================
# = Import general python modules                                           =
# ===========================================================================
from lxml import etree
import httplib

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