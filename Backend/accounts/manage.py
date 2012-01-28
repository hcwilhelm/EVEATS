from Backend.accounts.helper import AccountOperationResult
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core import serializers

import sys

def registerAccount(request):
    serializer = serializers.get_serializer("json")()
    response = HttpResponse(mimetype='application/json')

    username = request.REQUEST['username']
    password = request.REQUEST['password']
    email = request.REQUEST['email']

    result = AccountOperationResult(Success=True, Message="User created")

    try:
        user = User.objects.get(username=username)
        result.Success = False
        result.ErrorCode = 100
        result.Message = "Account already exists"
    except User.DoesNotExist:
        user = User(username=username, password=password, email=email)
        user.is_active = False
        user.is_staff = False
        user.is_superuser = False
        user.save()

    response.content = result
    return response