from django.contrib.auth.models import User
from django.contrib import auth

from django.http import HttpResponse
from django.core import serializers
from django.utils import simplejson
from django.core.validators import email_re

# =======================
# = ErrorMessage Object =
# =======================

class ErrorMessage(object):
    def __init__(self, success, message):
        self.success = success
        self.message = message
    
    def json(self):
        return simplejson.dumps({'success':self.success, 'message':self.message})

# ==============
# = login view =
# ==============
        
def login(request):
    response = HttpResponse(mimetype='application/json')
        
    if 'username' not in request.GET or 'password' not in request.GET:
        message = ErrorMessage(False, "Missing GET parameter! Usage: ?username=&password=")
        response.write(message.json())
        return response
        
    user = auth.authenticate(username=request.GET['username'], password=request.GET['password'])
    
    if user is None:
        message = ErrorMessage(False, "User not  found ! Register first")
        response.write(message.json());
        return response 
        
    else:
        if user.is_active:
            auth.login(request, user)
            message = ErrorMessage(True, "Login successful")
            response.write(message.json())
            return response
        
        else:
            message = ErrorMessage(False, "User not active ! Activate your account first")
            response.write(message.json())
            return response

# ===============
# = logout view =
# ===============

def logout(request):
    response = HttpResponse(mimetype='application/json')
    
    if request.user.is_authenticated():
        auth.logout(request)
        message = ErrorMessage(True, "Logout successful")
        response.write(message.json())
        
    else:
        message = ErrorMessage(False, "Login befor you logout")
        response.write(message.json())
    
    return response

# =================
# = register view =
# =================

def register(request):
    response = HttpResponse(mimetype='application/json')

    if 'email' not in request.GET or 'username' not in request.GET or 'password' not in request.GET or 'confirm' not in request.GET:
        message = ErrorMessage(False, "Missing GET paramater! Usage: ?email=&username=&password=&confirm=")
        response.write(message.json())
        return response
    
    if request.GET['username'] == "" or request.GET['password'] == "":
        message = ErrorMessage(False, "Username and Password can't be empty")
        response.write(message.json())
        return response

    if User.objects.filter(username=request.GET['username']).exists():
        message = ErrorMessage(False, "Username allready exists!")
        response.write(message.json())
        return response
 
    if not email_re.match(request.GET['email']):
        message = ErrorMessage(False, "Email dosen't look like a valid email address")
        response.write(message.json())
        return response

    if not request.GET['password'] == request.GET['confirm']:
        message = ErrorMessage(False, "Password confirm must be equal to password")
        response.write(message.json())
        return response

    user = User.objects.create_user(request.GET['username'], request.GET['email'], request.GET['password'])
    user.is_superuser = False
    user.is_stuff = False
    user.is_active = True
    user.save()
    
    message = ErrorMessage(True, "User created")
    reponse.write(message.json())
    return response

# =====================================================
# = listAccounts should be limeted to superusers only =
# =====================================================

def listAccounts(request):
    serializer = serializers.get_serializer("json")()
    response = HttpResponse(mimetype='application/json')

    result = User.objects.all()

    serializer.serialize(result, stream=response)
    return response