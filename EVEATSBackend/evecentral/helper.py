# ===========================================================================
# = Import general python modules                                           =
# ===========================================================================
from lxml import etree
import httplib

# ===========================================================================
# = Logging                                                                 =
# ===========================================================================
import logging
logger = logging.getLogger(__name__)

# =============================================================================
# = Helper functions                                                          =
# =============================================================================

def getXMLFromEveCentralAPI(action, params):
    header = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/xml"}

    connection = httplib.HTTPConnection("api.eve-central.com", 80)
    connection.request("GET", action, params, header)

    xml = connection.getresponse().read()
    connection.close()
    return etree.fromstring(xml)