# 
#  views.py
#  Backend
#  
#  Created by Hans Christian Wilhelm on 2012-02-17.
#  Copyright 2012 scienceondope.org All rights reserved.
# 


from eveapi.models import *
from eveapi.tasks import *

from django.contrib.auth.models import User
from django.contrib import auth

from django.core import serializers
from django.utils import simplejson

from django.http import HttpResponse
from django.views.decorators.cache import never_cache

def addAPIKey(request):
  response = HttpResponse(mimetype="application/json")
  
  if request.user.is_authenticated():
    if 'name' not in request.GET or 'keyID' not in request.GET or 'vCode' not in request.GET:
      response.write(simplejson.dumps({'success':False, 'message':"Missing GET parameter"}))
    else:
      request.user.apikey_set.create(keyID=request.GET['keyID'], vCode=request.GET['vCode'], name=request.GET['name'])
      response.write(simplejson.dumps({'success':True, 'message':"APIKey added"}))
  else:
    response.write(simplejson.dumps({'success':False, 'message':"You are not loged in"}))
    
  return response

@never_cache
def apiKeys(request):
  response = HttpResponse(mimetype="application/json")
  serializer = serializers.get_serializer("json")()
  
  if request.user.is_authenticated():
    result = request.user.apikey_set.all()
    serializer.serialize(result, stream=response)
    
  else:
    response.write(simplejson.dumps({'success':False, 'message':"You are not loged in"}))
    
  return response
  

@never_cache
def apiKeyInfo(request, apiKeyID):
  response = HttpResponse(mimetype="application/json")
  serializer = serializers.get_serializer("json")()
  
  if request.user.is_authenticated():
    apiKey = APIKey.objects.get(pk=apiKeyID)
    
    if apiKey.apiKeyInfo == None:
      result = ImportAPIKeyInfoTask.delay(apiKeyID)
      response.write(simplejson.dumps({'model':"Task", 'taskID':result.task_id}))
      
    elif apiKey.apiKeyInfo.expired():
      result = ImportAPIKeyInfoTask.delay(apiKeyID)
      response.write(simplejson.dumps({'model':"Task", 'taskID':result.task_id}))
      
    else:
      serializer.serialize([apiKey.apiKeyInfo], stream=response)
  
  else:
    response.write(simplejson.dumps({'success':False, 'message':"You are not loged in"}))
  
  return response
  
@never_cache
def characters(request, apiKeyID):
  response = HttpResponse(mimetype="application/json")
  serializer = serializers.get_serializer("json")()
  
  if request.user.is_authenticated():
    apiKey = APIKey.objects.get(pk=apiKeyID)
    
    chars = apiKey.characters_set.all()
    
    if len(chars) == 0:
      result = ImportCharactersTask.delay(apiKeyID)
      response.write(simplejson.dumps({'model':"Task", 'taskID':result.task_id}))
      
    else:
      needsUpdate = False
      
      for char in chars:
        if char.expired():
          needsUpdate = True
          break
          
      if needsUpdate:
        result = ImportCharactersTask.delay(apiKeyID)
        response.write(simplejson.dumps({'model':"Task", 'taskID':result.task_id}))
        
      else:
        result = apiKey.characters_set.all()
        serializer.serialize(result, stream=response)
  
  else:
     response.write(simplejson.dumps({'success':False, 'message':"You are not loged in"}))
     
  return response     