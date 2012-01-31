from Backend.helper import *
from Backend.eveapi.models import EveApiKey

from django.core import serializers
from django.contrib.auth.models import User
from django.http import HttpResponse

# =======================================================
#
# Add EVE Online API Key
#
# HTTP Parameters:
#   userID              = ID from user to save key for (optional, needs admin permissions)
#   keyID               = the key ID
#   keyVerificationCode = the verification code
#   comment             = comment to add to key
#
# Errorcodes:
#     0 = Key added
#   100 = not logged in
#   200 = API key already in database
#   300 = User for userID not found
#   400 = User not allowed to add keys for other users
#   900 = keyID parameter missing
#   901 = keyVerificationCode parameter missing
# =======================================================
def addApiKey(request):
    response = HttpResponse(mimetype='application/json')
    result = None
    if request.user.is_authenticated():
        userID = getHttpRequestParameter(request, 'userID')
        keyID = getHttpRequestParameter(request, 'keyID')
        keyVerificationCode = getHttpRequestParameter(request, 'keyVerificationCode')
        keyComment = getHttpRequestParameter(request, 'comment')

        if keyID is None:
            result = RequestResult(Message="keyID parameter missing", ErrorCode=900)
        elif keyVerificationCode is None:
            result = RequestResult(Message="keyVerificationCode parameter missing", ErrorCode=901)
        elif userID is not None and not (request.user.is_superuser or request.user.is_staff):
            result = RequestResult(Message="Missing permission to add keys for other users", ErrorCode=400)
        else:
            try:
                EveApiKey.objects.get(ccpID=keyID)
                result = RequestResult(Message="API Key already in database!", ErrorCode=200)
            except EveApiKey.DoesNotExist:
                thisUser = request.user
                if userID is not None:
                    try:
                        thisUser = User.objects.get(pk=userID)
                    except User.DoesNotExist:
                        thisUser = None
                        result = RequestResult(Message="User not found", ErrorCode=300)
                if thisUser is not None:
                    EveApiKey.objects.create(ccpID=keyID, verificationCode=keyVerificationCode, comment=keyComment, owner=thisUser)
                    result = RequestResult(Success=True, Message="API Key added")
    else:
        result = RequestResult(Message="You must login first", ErrorCode=100)
    response.content = result
    return response

# =======================================================
#
# List all EVE Online API Keys
#
# HTTP Parameters:
#   userID              = ID from user to save key for (optional, needs admin permissions)
#
# Errorcodes:
#   100 = not logged in
#   200 = User not allowed to view keys for other users
#   300 = User for userID not found
# =======================================================
def listApiKeys(request):
    serializer = serializers.get_serializer("json")()
    response = HttpResponse(mimetype='application/json')

    if request.user.is_authenticated():

        userID = getHttpRequestParameter(request, 'userID')

        if userID is None:
            result = EveApiKey.objects.filter(owner=request.user)
            serializer.serialize(result, stream=response)
        else:
            if request.user.is_superuser or request.user.is_staff:
                try:
                    thisUser = User.objects.get(pk=userID)
                    result = EveApiKey.objects.filter(owner=thisUser)
                    serializer.serialize(result, stream=response)
                except User.DoesNotExist:
                    response.content = RequestResult(Message="User not found", ErrorCode=300)

            else:
                response.content = RequestResult(Message="Missing permission to view keys for other users", ErrorCode=200)
    else:
        response.content = RequestResult(Message="You must login first", ErrorCode=100)

    return response