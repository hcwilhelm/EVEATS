from assets.models import *
from assets.tree import *

from django.http import HttpResponse
from django.core import serializers
from django.utils import simplejson


def marketGroups(request, id=None):
	serializer 	= serializers.get_serializer("json")()
	response 	= HttpResponse(mimetype='application/json')	
	result 		= None
	
	if (id == None):
		result = invMarketGroups.objects.filter(parentGroupID__isnull=True)
	
	else:
		result = invMarketGroups.objects.get(pk=id).invmarketgroups_set.all()

	serializer.serialize(result, relations=('iconID', ), stream=response)
	return response
	
def listEveIcons(request, id=None):
	serializer 	= serializers.get_serializer("json")()
	response 	= HttpResponse(mimetype='application/json')	
	result 		= None
	
	if (id == None):
		result = eveIcons.objects.all()
	
	else:
		result = [eveIcons.objects.get(pk=id)]
		
	serializer.serialize(result, ensure_ascii=False, stream=response)
	return response
	
def listCorpAssets(request, groupID=None):
	serializer 	= serializers.get_serializer("json")()
	response 	= HttpResponse(mimetype='application/json')	
	result 		= []
	
	if (groupID == None):
		result = invTypes.objects.all()[0:100];
		
	else:
		types = invMarketGroups.objects.get(pk=groupID).invtypes_set.all()			
		result = [ x for x in types if x.corpassetlist_set.all()]
		
	serializer.serialize(result, relations={'groupID':{'relations':('categoryID',)}}, extras=('units_available',), stream=response)
	return response
	
def listCorpAssetsByName(request):
	serializer 	= serializers.get_serializer("json")()
	response 	= HttpResponse(mimetype='application/json')
	
	result = set()
	
	if 'name' in request.GET and request.GET['name']:
		
		for item in corpAssetList.objects.filter(typeID__typeName__icontains=request.GET['name'])[0:50]:
			result.add(item.typeID)

	serializer.serialize(result, relations={'groupID':{'relations':('categoryID',)}}, extras=('units_available',), stream=response)
	return response
	
def getTreeForTypeID(request, ID):
	serializer 	= serializers.get_serializer("json")()
	response 	= HttpResponse(mimetype='application/json')	
 	
	items		= corpAssetList.objects.filter(typeID = ID)
	paths		= [ x.get_path() for x in items]

	root 	= Node()
	
	for path in paths:		
		path.reverse()

		for item in path:
			node = root.find(item)
			
			if not node:
				node = root.find(item.parentID)
				
				if node:
					node.insert(item)
					
				else:
					root.insert(item)

	root.create_quantity()	
	response 	= HttpResponse(simplejson.dumps(root.serializable_object()), mimetype='application/json')	
	return response
	
	
		
		
		