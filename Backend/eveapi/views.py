# 
#  views.py
#  Backend
#  
#  Created by Hans Christian Wilhelm on 2012-02-17.
#  Copyright 2012 scienceondope.org All rights reserved.
# 


from eveapi.models import *
from eveapi.tasks import *
from celery.task.sets import TaskSet

from django.contrib.auth.models import User
from django.contrib import auth

from django.core import serializers
from django.utils import simplejson

from django.http import HttpResponse
from django.views.decorators.cache import never_cache

@never_cache
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
def removeAPIKey(request):
  response = HttpResponse(mimetype="application/json")
  
  if request.user.is_authenticated():
    if 'keyID' not in request.GET:
      response.write(simplejson.dumps({'success':False, 'message':"Missing GET parameter"}))
      return response
    
    apiKey = APIKey.objects.get(pk=request.GET['keyID'])
    
    if apiKey not in request.user.apikey_set.all():
      response.write(simplejson.dumps({'success':False, 'message':"This APIKey is not related to your account"}))
      return response
      
    else:
      apiKey.delete()
      response.write(simplejson.dumps({'success':True, 'message':"APIKey removed"}))
      return response
  
  else:
    response.write(simplejson.dumps({'success':False, 'message':"You are not loged in"}))
    return response 
  

@never_cache
def apiKeys(request):
  response = HttpResponse(mimetype="application/json")
  serializer = serializers.get_serializer("json")()
  
  if request.user.is_authenticated():
    
    keys = request.user.apikey_set.all()
    tasks = []
    
    for key in keys:
      if key.valid == None or not key.valid or key.apiKeyInfo == None:
        key.characters_set.all().delete()
        
        tasks.append(ImportAPIKeyInfoTask.subtask((key.id,)))
        
      elif key.apiKeyInfo.expired():
        key.characters_set.all().delete()
        key.apiKeyInfo.delete()
        
        key.apiKeyInfo = None
        key.save()
        
        tasks.append(ImportAPIKeyInfoTask.subtask((key.id,)))
    
    job = TaskSet(tasks=tasks)
    job.apply_async().join()
    
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
    
    if apiKey.valid:
      serializer.serialize([apiKey.apiKeyInfo], stream=response)
      
    else:
      response.write(simplejson.dumps({'success':False, 'message':"APIKey is not Valid"}))
  
  else:
    response.write(simplejson.dumps({'success':False, 'message':"You are not loged in"}))
  
  return response
  
@never_cache
def characters(request):
  response = HttpResponse(mimetype="application/json")
  serializer = serializers.get_serializer("json")()
  
  if request.user.is_authenticated():
    
    result = []
    keys = request.user.apikey_set.all()
    
    for key in keys:
      if key.valid:
        result.extend(key.characters_set.all())
    
    serializer.serialize(result, stream=response)
  
  else:
     response.write(simplejson.dumps({'success':False, 'message':"You are not loged in"}))
     
  return response     