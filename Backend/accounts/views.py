from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core import serializers

def listAccounts(request):
    serializer = serializers.get_serializer("json")()
    response = HttpResponse(mimetype='application/json')

    result = User.objects.all()

    serializer.serialize(result, stream=response)
    return response