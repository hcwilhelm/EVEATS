# 
#  client.py
#  Backend
#  
#  Created by Hans Christian Wilhelm on 2012-02-10.
#  Copyright 2012 scienceondope.org All rights reserved.
# 

# =========================
# = import python modules =
# =========================

import httplib
import urllib

# =============================
# = Static eve api Host/Port  =
# =============================

EVE_API_HOST = "api.eveonline.com"
EVE_API_PORT = 446

# ===================
# = Excpetion class =
# ===================

class EVEError(Exception):
  
  def __init__(self, code, error):
    self.code   = code
    self.error  = error

# ==============================================
# = Class EVEClient used to query the EVE API  =
# = Return value is a plain XML String         =
# ==============================================

class EVEClient(object):
  
  def __init__(self, apiKey):
    self.apiKey = apiKey
    
  def getAPIKeyInfo(self):
    action = "/account/APIKeyInfo.xml.aspx"
    params = urllib.urlencode({'keyID':self.apiKey.keyID, 'vCode':self.apiKey.vCode})
    header = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    
    connection = httplib.HTTPSConnection(EVE_API_HOST, EVE_API_PORT)
    connection.request("GET", action, params, header)
    
    xml = connection.getresponse().read()
    connection.close()
    
    return xml