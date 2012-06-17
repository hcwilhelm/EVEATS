from django.utils import simplejson
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required

from evedb.models import invTypes, invMarketGroups
from common.helper import func_logger as logger

# ==============================================
# = Simple Views to access the EVE static dump =
# ==============================================

@cache_page(60 * 60 * 24)
@login_required(login_url="/common/authentificationError")
def inv_type(request, typeID):
    response = HttpResponse(mimetype="application/json")
    
    result = invTypes.objects.values().get(pk=typeID)    
    response.write(simplejson.dumps(result, indent=2))
    
    logger.debug("User %s requested inv_typ %s" % (request.user.username, typeID))
    return response
  
@cache_page(60 * 60 * 24)
@login_required(login_url="/common/authentificationError")  
def inv_market_group(request, marketGroupID):
    response = HttpResponse(mimetype="application/json")

    result = invMarketGroups.objects.values().get(pk=marketGroupID)
    response.write(simplejson.dumps(result, indent=2))

    logger.debug("User %s requested inv_market_group %s" % (request.user.username, marketGroupID))
    return response

#@cache_page(60 * 60 * 24)
@login_required(login_url="/common/authentificationError")  
def inv_market_group_tree(request):
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