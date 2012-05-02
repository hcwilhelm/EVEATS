# 
#  views.py
#  Backend
#  
#  Created by Hans Christian Wilhelm on 2012-04-24.
#  Copyright 2012 scienceondope.org All rights reserved.
# 


from django.utils import simplejson
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

from evedb.models import *

# ==============================================
# = Simple Views to access the EVE static dump =
# ==============================================

@cache_page(60 * 60 * 24)
def invType(request, typeID):
  response = HttpResponse(mimetype="application/json")
  
  result = invTypes.objects.values().get(pk=typeID)
  
  response.write(simplejson.dumps(result, indent=2))
  return response
  
@cache_page(60 * 60 * 24)  
def invMarketGroup(request, marketGroupID):
  response = HttpResponse(mimetype="application/json")
  
  result = invMarketGroups.objects.values().get(pk=marketGroupID)
  
  response.write(simplejson.dumps(result, indent=2))
  return response

#@cache_page(60 * 60 * 24)  
def invMarketGroupTree(request):
  response = HttpResponse(mimetype="application/json")
  
  expand = lambda obj: {
    "marketGroupID":obj.marketGroupID, 
    "marketGroupName":obj.marketGroupName,
    "description":obj.description,
    "iconID":(obj.iconID.iconFile if obj.iconID != None else None),
    "hasTypes":obj.hasTypes,
    "childs":[expand(x) for x in obj.invmarketgroups_set.all()]
  }
  
  groups = [expand(x) for x in invMarketGroups.objects.filter(parentGroupID=None)]
  
  response.write(simplejson.dumps(groups, indent=2))
  return response