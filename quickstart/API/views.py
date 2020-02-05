from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from quickstart.models import UserDetails,UserGroup
from quickstart.API.serializer import UserDetailsSerializers,UserGroupSerializer


@api_view(['GET'])
def get_user_details(self,request):
    return Response(request)


@api_view(['POST'])
def add_user_details(request):
    ##serilizer = UserGroupSerializer(data=request.data)
    data=request.data
    return Response(data)
