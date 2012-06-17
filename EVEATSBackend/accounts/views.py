from django.contrib.auth.models import User
from django.contrib import auth

from django.http import HttpResponse
from django.core import serializers
from django.utils import simplejson
from django.core.validators import email_re

from django.views.decorators.cache import never_cache

from django.core.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt

# import the logging stuff
from common.helper import func_logger as logger

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
@never_cache
@csrf_exempt
@ensure_csrf_cookie
def login(request):
  response = HttpResponse(mimetype='application/json')  
  auth.logout(request);
      
  if 'username' not in request.POST or 'password' not in request.POST:
    message = ErrorMessage(False, "Missing POST parameter!")
    response.write(message.json())
    logger.error("Invalid login: Username or password not set.")
    return response
      
  user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
  
  if user is None:
    message = ErrorMessage(False, "User not  found! Register first")
    response.write(message.json());
    logger.warning("User %s tried to login, but account does not exists!" % request.POST['username'])
    return response     
  
  else:
    if user.is_active:
      auth.login(request, user)
      message = ErrorMessage(True, "Login successful")
      response.write(message.json())
      logger.info("Login successful for user %s" % user)
      return response    
    
    else:
      message = ErrorMessage(False, "User not active! Activate your account first")
      response.write(message.json())
      logger.warning("User %s tried to login, but is not activated yet!" % user)
      return response

# ===============
# = logout view =
# ===============
@never_cache
def logout(request):
  response = HttpResponse(mimetype='application/json')
  
  if request.user.is_authenticated():
    username = request.user.username
    auth.logout(request)
    message = ErrorMessage(True, "Logout successful")
    response.write(message.json())
    logger.info("User %s logged out" % username)
      
  else:
    message = ErrorMessage(False, "You must login before you logout")
    response.write(message.json())
    logger.error("User tried to logout but wasn't logged in.")
  
  return response

# =================
# = register view =
# =================
@never_cache
@csrf_exempt
def register(request):
  response = HttpResponse(mimetype='application/json')

  if 'email' not in request.POST or 'username' not in request.POST or 'password' not in request.POST or 'confirm' not in request.POST:
    message = ErrorMessage(False, "Missing POST paramater! Usage: ?email=&username=&password=&confirm=")
    response.write(message.json())
    return response
  
  if request.POST['username'] == "" or request.POST['password'] == "":
    message = ErrorMessage(False, "Username and Password can't be empty")
    response.write(message.json())
    return response

  if User.objects.filter(username=request.POST['username']).exists():
    message = ErrorMessage(False, "Username allready exists!")
    response.write(message.json())
    return response

  if not email_re.match(request.POST['email']):
    message = ErrorMessage(False, "Email dosen't look like a valid email address")
    response.write(message.json())
    return response

  if not request.POST['password'] == request.POST['confirm']:
    message = ErrorMessage(False, "Password confirm must be equal to password")
    response.write(message.json())
    return response

  user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
  user.is_superuser = False
  user.is_stuff = False
  user.is_active = True
  user.save()
   
  message = ErrorMessage(True, "User created")
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

# =====================================================
# = list_accounts should be limeted to superusers only =
# =====================================================
@never_cache
def list_accounts(request):
  serializer = serializers.get_serializer("json")()
  response = HttpResponse(mimetype='application/json')
  
  result = User.objects.all()
  
  serializer.serialize(result, stream=response)
  return response