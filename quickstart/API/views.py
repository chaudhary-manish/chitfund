from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
#from quickstart.models import *
#from quickstart.API.serializer import UserDetails


@api_view(['GET'])
def get_user_details(self):
    return Response('HI manish')
