#
#  views.py
#  Backend
#
#  Created by Hans Christian Wilhelm on 2012-02-17.
#  Copyright 2012 scienceondope.org All rights reserved.
#

#
from eve.models import *
from eve.tasks import *

from django.contrib.auth.models import User
from django.contrib import auth

from django.http import HttpResponse

import simplejson as json


# ==========================
# = Common Response Class  =
# ==========================

#
# The JSONResponse class is used in every view !
# If an Error occurs you set success=False and append a message
# If all went fine you can pass the result or you pass a taskID
# to inform the Frontend that some long running work is in progress.
#

class JSONResponse:
  def __init__(self, success=True, message=None, result=None, taskID=None):
    self.success = success
    self.message = message
    self.result  = result
    self.taskID  = taskID

  def json(self):
    return json.dumps({"success":self.succsess, "message":self.message, "result":self.result, "taskID":self.taskID})

# ======================
# = APIKey Operations  =
# ======================

def addAPIKey(request):
  response = HttpResponse(mimetype="application/json")

  if not request.user.is_authenticated():
    jsonResponse = JSONResponse(success=False, message="You are not logged in")
    response.write(jsonResponse.json())

    return response

  if request.user.is_authenticated():
    result = AddAPIKeyTask.delay(request.user.id, request.POST["name"], request.POST["keyID"], request.POST["vCode"])

    jsonResponse = JSONResponse(success=True, taskID=result.task_id)
    response.write(jsonResponse.json())

    return response

def removeAPIKey(request):
  response = HttpResponse(mimetype="application/json")

  if not request.user.is_authenticated():
    jsonResponse = JSONResponse(success=False, message="You are not logged in")
    response.write(jsonResponse.json())

    return response

  if request.user.is_authenticated():
    result = RemoveAPIKeyTask.delay(request.user.id, request.POST["keyID"])

    jsonResponse = JSONResponse(success=True, taskID=result.task_id)
    response.write(jsonResponse.json())

    return response


def listAPIKey(request):
  response = HttpResponse(mimetype="application/json")

  if not request.user.is_authenticated():
    jsonResponse = JSONResponse(success=False, message="You are not logged in")
    response.write(jsonResponse.json())

    return response

  if request.user.is_authenticated():
    result = ListAPIKeyTask.delay(request.user.id)

    jsonResponse = JSONResponse(success=True, taskID=result.task_id)
    response.write(jsonResponse.json())

    return response

# ==================
# = Get APIKeyInfo =
# ==================

def apiKeyInfo(request, apiKeyID):
  response = HttpResponse(mimetype="application/json")
  serializer = serializers.get_serializer("json")()

  if request.user.is_authenticated():
    apiKey = APIKey.objects.get(pk=apiKeyID)

    if apiKey.apiKeyInfo == None:
      taskResult = UpdateAPIKeyInfoTask.delay(apiKey.id)
      taskResult.get()

    elif apiKey.apiKeyInfo.expired()
      taskResult = UpdateAPIKeyInfoTask.delay(apiKey.id)
      taskResult.get()

    if apiKey.valid:
      serializer.serialize([apiKey.apiKeyInfo], stream=response)

    else:
      response.write(simplejson.dumps({'success':False, 'message':"APIKey is not Valid"}))

  else:
    response.write(simplejson.dumps({'success':False, 'message':"You are not loged in"}))

  return response

