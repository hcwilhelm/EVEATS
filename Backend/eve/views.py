#
#  views.py
#  Backend
#
#  Created by Hans Christian Wilhelm on 2012-02-17.
#  Copyright 2012 scienceondope.org All rights reserved.
#
#

from common.views import JSONResponse
from eve.models import *
from eve.tasks import *

from django.db.models import Avg, Max, Min, Count
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

from celery.task.sets import TaskSet

# ======================
# = APIKey Operations  =
# ======================

@login_required(login_url="/common/authentificationError")
def addAPIKey(request):
  response = HttpResponse(mimetype="application/json")

  keyID = request.POST["keyID"]
  vCode = request.POST["vCode"]
  name  = request.POST["name"]
  user  = request.user

  apiKey = APIKey(keyID=keyID, vCode=vCode, name=name, user=user)
  apiKey.save()

  updateAPIKey.delay(apiKey.pk)

  jsonResponse = JSONResponse()
  response.write(jsonResponse.json())

  return response

@login_required(login_url="/common/authentificationError")
def removeAPIKey(request):
  response = HttpResponse(mimetype="application/json")

  keyID = response.POST["keyID"]
  APIKey.objects.filter(pk=keyID).delete()

  jsonResponse = JSONResponse(success=True)
  response.write(jsonResponse.json())

  return response

@login_required(login_url="/common/authentificationError")
def apiKeys(request):
  response = HttpResponse(mimetype="application/json")

  keys  = request.user.apikey_set.all()
  tasks = []

  for key in keys:
    if key.expired():
      tasks.append(updateAPIKey.subtask([key.pk]))

  job     = TaskSet(tasks=tasks)
  result  = job.apply_async()

  print result.join()

  keys  = request.user.apikey_set.all()
  jsonResponse = JSONResponse(success=True, result=keys)

  response.write(jsonResponse.json())
  return response

# ======================================
# = Character / Corporation operations =
# ======================================


#
# Returns all Characters associated to your APIKey's
#

@login_required(login_url="/common/authentificationError")
def characters(request):
  response = HttpResponse(mimetype="application/json")

  tasks = []

  for key in request.user.apikey_set.all():
    for char in key.character_set.all():
      if char.expired():
        tasks.append(updateCharacter.subtask([char.pk]))

  job = TaskSet(tasks=tasks)
  result = job.apply_async()

  print result.join()

  chars = Character.objects.none()

  for key in request.user.apikey_set.all():
    chars = chars | key.character_set.all()

  jsonResponse = JSONResponse(success=True, result=chars)

  response.write(jsonResponse.json())
  return response

#
# Returns all Corporations associated to your APIKey's
#

@login_required(login_url="/common/authentificationError")
def corporations(request):
  response = HttpResponse(mimetype="application/json")

  tasks = []

  for key in request.user.apikey_set.all():
    for corp in key.corporation_set.all():
      if corp.expired():
        tasks.append(updateCorporation.subtask([corp.pk]))

  job = TaskSet(tasks=tasks)
  result = job.apply_async()

  print result.join()

  corps = Corporation.objects.none()

  for key in request.user.apikey_set.all():
    corps = corps | key.corporation_set.all()

  jsonResponse = JSONResponse(success=True, result=corps)

  response.write(jsonResponse.json())
  return response


# ================
# = Query Assets =
# ================

from functools import wraps

#
# This Decorater makes sure the User has permission
# to query assets for a Character. It also checks if
# the Characters exists or if the Character assets need
# to be updated
#

def character_permission_required(function):
  @wraps(function)
  def wrapper(request, charID, *args, **kwargs):
    
    response  = HttpResponse(mimetype="application/json")
    char      = None
    
    try:
      char = Character.objects.get(pk=charID)
    
    except Exception, e:
      jsonResponse = JSONResponse(success=False, message=str(e))
      response.write(jsonResponse.json())
      return response
    
    if not request.user.has_perm('eve.viewAssetList_character', char):
      jsonResponse = JSONResponse(success=False, message="You don't have permission")
      response.write(jsonResponse.json())
      return response
      
    if char.assetList == None:
      result = updateAssetList.delay(char.pk, "Character")

      jsonResponse = JSONResponse(success=True, taskID=result.task_id)
      response.write(jsonResponse.json())
      return response
      
    if char.assetList.expired():
      result = updateAssetList.delay(char.pk, "Character")

      jsonResponse = JSONResponse(success=True, taskID=result.task_id)
      response.write(jsonResponse.json())
      return response
      
    else:
      return function(request, charID, *args, **kwargs)
    
  return wrapper


@login_required(login_url="/common/authentificationError")
@character_permission_required
def characterAssetsByMarketGroup(request, charID, marketGroupID=None):
  response = HttpResponse(mimetype="application/json")

  char = Character.objects.get(pk=charID)
  
  expand = lambda obj: {
    "typeID":obj['typeID'], 
    "typeName": invTypes.objects.get(pk=obj['typeID']).typeName,
    "locationName":mapDenormalize.objects.get(pk=obj['locationID']).itemName,
    "locationID":obj['locationID'],
    "quantity":obj['total'],
  }
  
  if marketGroupID == None:
    assets = char.assetList.asset_set.filter(typeID__marketGroupID = marketGroupID).values('typeID','locationID').annotate(total = Count('quantity')).order_by('-total')
    
    result = [expand(x) for x in assets]
    jsonResponse = JSONResponse(success=True, result=result)
    response.write(jsonResponse.json())
  
  else:
    assets = char.assetList.asset_set.filter(typeID__marketGroupID = marketGroupID).values('typeID','locationID').annotate(total = Count('quantity')).order_by('-total')
    
    result = [expand(x) for x in assets]
    jsonResponse = JSONResponse(success=True, result=result)
    response.write(jsonResponse.json())

  return response

@login_required(login_url="/common/authentificationError")
@character_permission_required
def characterAssetsByTypeName(request, charID, typeName=""):
  response = HttpResponse(mimetype="application/json")

  char = Character.objects.get(pk=charID)
  
  expand = lambda obj: {
    "typeID":obj['typeID'], 
    "typeName": invTypes.objects.get(pk=obj['typeID']).typeName,
    "locationName":mapDenormalize.objects.get(pk=obj['locationID']).itemName,
    "locationID":obj['locationID'],
    "quantity":obj['total'],
  }
  
  assets = char.assetList.asset_set.filter(typeID__typeName__icontains = typeName).values('typeID','locationID').annotate(total = Count('quantity')).order_by('-total')[:10]
  
  result = [expand(x) for x in assets]
  jsonResponse = JSONResponse(success=True, result=result)
  response.write(jsonResponse.json())
  
  return response
  
  
# =====================================================
# = Tree Class, helper to build the Assets DetailView =
# =====================================================  

class Node:
  def __init__(self, data="root"):
    self.data     = data
    self.childs   = []
    
  def insert(self, data):
    self.childs.append(Node(data))
    
  def find(self, data):
    
    if self.data == data:
      return self
    
    else:
      for child in self.childs:
        return child.find(data)
    
    return None
  
  
@login_required(login_url="/common/authentificationError")
@character_permission_required
def characterAssetsDetailTree(request, charID, typeID, locationID):
  response = HttpResponse(mimetype="application/json")
  
  char    = Character.objects.get(pk=charID)
  assets  = char.assetList.asset_set.filter(typeID=typeID, locationID=locationID)
  
  paths   = [x.getPath() for x in assets]
  root    = Node(locationID)
  
  for path in paths:
    path.reverse()
    
    for asset in path:
      node = root.find(asset)
      
      if not node:
        node = root.find(asset.parent)

        if node:
          node.insert(asset)
          
        else:
          root.insert(asset)
  
  
  expand = lambda obj: {
    "typeID":obj.data.typeID_id, 
    "typeName":obj.data.typeID.typeName,
    "flag":obj.data.flag.flagName,
    "quantity":obj.data.quantity,
    "childs":[expand(x) for x in obj.childs],
  }
  
  result = [expand(x) for x in root.childs]
  jsonResponse = JSONResponse(success=True, result=result)
  response.write(jsonResponse.json())
  
  return response
  
  