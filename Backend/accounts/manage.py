from Backend.accounts.helper import RequestResult
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.validators import email_re

# =======================================================
#
# Login function, creates session for user, too
#
# HTTP Parameters:
#   username    = the username
#   password    = the password
#   email       = the email
#
# Errorcodes:
#     0 = Account created
#   100 = Account already exists
#   200 = Already authenticated
#   900 = Username missing
#   901 = Password missing
#   902 = Email missing
#   903 = Email invalid
# =======================================================
def registerAccount(request):
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

        try:
            email = request.REQUEST['email']
            if not email_re.match(email):
                result = RequestResult( Message="Invlaid email", ErrorCode=903)
                response.content = result
                return response
        except KeyError:
            result = RequestResult( Message="Unable to find email", ErrorCode=902)
            response.content = result
            return response

        if result is None:
            result = RequestResult(Success=True, Message="User created")

            try:
                User.objects.get(username=username)
                result.Success = False
                result.ErrorCode = 100
                result.Message = "Account already exists"
            except User.DoesNotExist:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.is_active = False
                user.is_staff = False
                user.is_superuser = False
                user.save()

    response.content = result
    return response