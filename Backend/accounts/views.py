from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse
from django.core import serializers
from Backend.helper import RequestResult

def listAccounts(request):
    serializer = serializers.get_serializer("json")()
    response = HttpResponse(mimetype='application/json')

    result = User.objects.all()

    serializer.serialize(result, stream=response)
    return response

# =======================================================
#
# Login function, creates session for user, too
#
# HTTP Parameters:
#   username = the username
#   password = the password
#
# Errorcodes:
#     0 = Login successful
#   100 = Login failed
#   200 = Account disabled
#   300 = Already authenticated
#   900 = Username missing
#   901 = Password missing
# =======================================================
def login(request):
    response = HttpResponse(mimetype='application/json')
    result = None

    if request.user.is_authenticated():
        result = RequestResult(ErrorCode=300, Message="Already authenticated - Please logout first!")
    else:
        try:
            username = request.REQUEST['username']
        except KeyError:
            result = RequestResult(Message="Unable to find username", ErrorCode=900)
            response.content = result
            return response

        try:
            password = request.REQUEST['password']
        except KeyError:
            result = RequestResult( Message="Unable to find password", ErrorCode=901)
            response.content = result
            return response

        if result is None:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    result = RequestResult(Success=True, Message="Login successful")
                else:
                    result = RequestResult(Message="Account disabled", ErrorCode=200)
            else:
                result = RequestResult(Message="Login failed", ErrorCode=100)
    response.content = result
    return response

# =======================================================
#
# Logout, removes user from session, too
#
# Errorcodes:
#     0 = Login successful
#   100 = Logout failed
# =======================================================
def logout(request):
    response = HttpResponse(mimetype='application/json')
    if request.user.is_authenticated():
        auth.logout(request)
        result = RequestResult(Success=True, Message="Logout successful")
    else:
        result = RequestResult(Message="You must login first to logout, right?", ErrorCode=100)
    response.content = result
    return response