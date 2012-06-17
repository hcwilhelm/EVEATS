from django.contrib.auth.models import User
from django.contrib import auth

from django.http import HttpResponse

from django.utils import simplejson

from django.core import serializers
from django.core.validators import email_re

from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt

# import the logging stuff
from common.helper import func_logger as logger
from common.views import JSONResponse 

# ==============
# = login view =
# ==============
@never_cache
@csrf_exempt
@ensure_csrf_cookie
def login(request):
    """Allow a user to login
    
    Used HTTP POST variables:
    username     - the username
    password     - the password
    """
    response = HttpResponse(mimetype='application/json')  
    auth.logout(request);
        
    if 'username' not in request.POST or 'password' not in request.POST:
        message = JSONResponse(success=False, message="Missing POST parameter!")
        response.write(message.json())
        logger.error("Invalid login: Username or password not set.")
        return response
        
    user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
    
    if user is None:
        message = JSONResponse(success=False, message="Login failed!")
        response.write(message.json());
        logger.warning("User %s tried to login, but login failed (wrong password or account does not exists)" % request.POST['username'])
        return response     
    
    else:
        if user.is_active:
            auth.login(request, user)
            message = JSONResponse(success=True, message="Login successful")
            response.write(message.json())
            logger.info("Login successful for user %s" % user)
            return response    
      
        else:
            message = JSONResponse(success=False, message="User not active! Activate your account first")
            response.write(message.json())
            logger.warning("User %s tried to login, but is not activated yet!" % user)
            return response

# ===============
# = logout view =
# ===============
@never_cache
def logout(request):
    """simply logout the current user"""
    response = HttpResponse(mimetype='application/json')
    
    if request.user.is_authenticated():
        username = request.user.username
        auth.logout(request)
        message = JSONResponse(success=True, message="Logout successful")
        response.write(message.json())
        logger.info("User %s logged out" % username)
        
    else:
        message = JSONResponse(success=False, message="You must login before you logout")
        response.write(message.json())
        logger.error("User tried to logout but wasn't logged in.")
    
    return response

# =================
# = register view =
# =================
@never_cache
@csrf_exempt
def register(request):
    """allows a user to register
    
    Used HTTP POST variables:
    username     - the username
    password     - the password
    confirm      - the password again
    email        - the email address
    """
    response = HttpResponse(mimetype='application/json')
    
    if 'email' not in request.POST or 'username' not in request.POST or 'password' not in request.POST or 'confirm' not in request.POST:
        message = JSONResponse(success=False, message="Missing POST paramater! ")
        response.write(message.json())
        return response
    
    if request.POST['username'] == "" or request.POST['password'] == "":
        message = JSONResponse(success=False, message="Username and Password can't be empty")
        response.write(message.json())
        return response
    
    if User.objects.filter(username=request.POST['username']).exists():
        message = JSONResponse(success=False, message="Username already exists!")
        response.write(message.json())
        return response
    
    if not email_re.match(request.POST['email']):
        message = JSONResponse(success=False, message="Email dosen't look like a valid email address")
        response.write(message.json())
        return response
    
    if not request.POST['password'] == request.POST['confirm']:
        message = JSONResponse(success=False, message="Password confirm must be equal to password")
        response.write(message.json())
        return response
    
    user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
    user.is_superuser = False
    user.is_stuff = False
    user.is_active = True
    user.save()
     
    message = JSONResponse(success=True, message="User created")
    response.write(message.json())
    return response

# =============
# = info View =
# =============
@never_cache
def info(request):
    serializer = serializers.get_serializer("json")()
    response = HttpResponse(mimetype='application/json')
    
    serializer.serialize([request.user], stream=response)
    return response

# ======================================================
# = list_accounts should be limited to superusers only =
# ======================================================
@never_cache
def list_accounts(request):
    serializer = serializers.get_serializer("json")()
    response = HttpResponse(mimetype='application/json')
    
    result = User.objects.all()
    
    serializer.serialize(result, stream=response)
    return response