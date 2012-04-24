# ==========================
# = Common Response Class  =
# ==========================

from django.http                    import HttpResponse
from django.core                    import serializers
from django.utils                   import simplejson
from django.db.models.query         import QuerySet
from django.core.serializers.json   import DjangoJSONEncoder

class HandleQuerySets(DjangoJSONEncoder):
  def default(self, obj):
    if type(obj) == QuerySet:
      return serializers.serialize("python", obj, ensure_ascii=False)
    return DjangoJSONEncoder.default(self, obj)

#
# The JSONResponse class is used in every view !
# If an Error occurs you set success=False and append a message
# If all went fine you can pass the result or you pass a taskID
# to inform the Frontend that some long running work is in progress.

class JSONResponse:
  def __init__(self, success=True, message=None, result=None, taskID=None):
    self.success = success
    self.message = message
    self.result = result
    self.taskID = taskID

  def json(self):
    return simplejson.dumps(
        {"success": self.success, "message": self.message, "result": self.result, "taskID": self.taskID},
      cls=HandleQuerySets, indent=2)


def authentificationError(request):
  response = HttpResponse(mimetype="application/json")

  jsonResponse = JSONResponse(success=False, message="You are not logged in")
  response.write(jsonResponse.json())

  return response
