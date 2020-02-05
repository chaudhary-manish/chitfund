from rest_framework import serializers
from quickstart.models import UserGroup

class UserGroup(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = ['id', 'groupname', 'startDate', 'usercount', 'createBy', 'isActive','AmountPerUser','sarkriGhata','groupbiddingtype']
