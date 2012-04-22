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

from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.utils import simplejson

from django.db.models.query import QuerySet
from celery.task.sets import TaskSet

class HandleQuerySets(DjangoJSONEncoder):
  def default(self, obj):
    if type(obj) == QuerySet:
      return serializers.serialize("python", obj, ensure_ascii=False)
    return DjangoJSONEncoder.default(self, obj)

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

@login_required(login_url="/common/authentificationError")
def characterAssets(request, ID):
  response = HttpResponse(mimetype="application/json")

  char = None

  try:
    char = Character.objects.get(pk=ID)

  except Exception, e:
    jsonResponse = JSONResponse(success=False, message=str(e))
    response.write(jsonResponse.json())
    return response

  taskResult = None

  if request.user.has_perm('eve.viewAssetList_character', char):
    if char.assetList is None:
     taskResult = updateAssetList.delay(char.pk, Character)

    elif char.assetList.expired():
      taskResult = updateAssetList.delay(char.pk, Character)

    if taskResult is not None:
      if taskResult.get():
        char = Character.objects.get(pk=ID)
        assets = char.assetList.asset_set.all()
        jsonResponse = JSONResponse(success=True, result=assets)
        response.write(jsonResponse.json())

      else:
        jsonResponse = JSONResponse(success=False, message="Assets import Error")
        response.write(jsonResponse.json())

    else:
      assets = char.assetList.asset_set.all()
      jsonResponse = JSONResponse(success=True, result=assets)
      response.write(jsonResponse.json())


  return response


