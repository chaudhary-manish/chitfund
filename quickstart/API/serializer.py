from rest_framework import serializers
from quickstart.models import UserDetails

class UserDetailsSerializers(serializers.ModelSerializer):
    class Meta:
        model =UserDetails
        fields = ['id', 'groupname', 'startDate', 'usercount',
         'createBy', 'isActive','AmountPerUser','sarkriGhata','groupbiddingtype']
