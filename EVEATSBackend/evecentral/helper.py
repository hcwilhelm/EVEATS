# ===========================================================================
# = Import general python modules                                           =
# ===========================================================================
from lxml import etree
import httplib

# =============================================================================
# = Helper functions                                                          =
# =============================================================================

def getXMLFromEveCentralAPI(action, params):
    header = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    
    connection = httplib.HTTPConnection("api.eve-central.com", 80)
    connection.request("GET", action, params, header)
    
    xml = connection.getresponse().read()
    connection.close()
    
    if xml.lower() == "Can't find that type":
        return None
    else:
        return etree.fromstring(xml)