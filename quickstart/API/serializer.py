from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from quickstart.models import UserDetails,GroupMember
from django.contrib.auth.models import User
from rest_framework import exceptions
from quickstart.models import *


class RegisterSerializer(serializers.Serializer):    
    MobileNumber = serializers.CharField()
    Firstname = serializers.CharField()
    LastName = serializers.CharField()
    Email = serializers.CharField()
    Password = serializers.CharField()


    def validate(self, data):
        username = data.get("MobileNumber", "")
        Firstname = data.get("Firstname", "")
        LastName = data.get("LastName", "")
        Email = data.get("Email", "")
        Password = data.get("Password", "")

        if username and Password and Firstname and LastName:
            user = User(username=username, password=Password,
            first_name=Firstname,last_name=LastName,email=Email)
            user.set_password(Password)
            user.save()
            data['user']=user           
        else:
            msg = "Must provide username and password FirstName and LastName both."
            raise exceptions.ValidationError(msg)
        return data


class LoginSerializer(serializers.Serializer):    
    MobileNumber = serializers.CharField()
    Password = serializers.CharField()


    def validate(self, data):
        MobileNumber = data.get("MobileNumber", "")     
        Password = data.get("Password", "")

        if MobileNumber and Password:
            user = authenticate(username=MobileNumber, password=Password)
            print(user)
            if user is not None:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "User is deactivated."
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Unable to login with given credentials."+ make_password(Password)
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide username and password both."
            raise exceptions.ValidationError(msg)
        return data

class AddGroupSerializer(serializers.Serializer):    
    GroupName = serializers.CharField()
    AmountPaidByUser = serializers.FloatField()
    SarkariGhata = serializers.FloatField()
    TotalUser = serializers.IntegerField()
    StartDate = serializers.DateField()
    GroupBiddingType = serializers.IntegerField()


    def validate(self,data):
        GroupName = data.get("GroupName", "")
        AmountPaidByUser = data.get("AmountPaidByUser", "")
        SarkariGhata = data.get("SarkariGhata", "")
        TotalUser = data.get("TotalUser", "")
        StartDate = data.get("StartDate","")
        GroupBiddingType = data.get("GroupBiddingType", "")
        user_id = self.context["user_id"]
        userdetail =User.objects.get(id = user_id)

        if GroupBiddingType and StartDate and TotalUser and SarkariGhata and AmountPaidByUser and GroupName:
            NewGroup =UserGroup(groupname=GroupName ,startDate=StartDate,usercount= TotalUser
                             ,createBy=user_id,AmountPerUser= AmountPaidByUser,sarkriGhata=SarkariGhata,
                             groupbiddingtype=GroupBiddingType,isActive=1)
            NewGroup.save()
            NewGroupUser =GroupMember(UserGroup=NewGroup.pk,Mobilenumber=userdetail.username,UserName=userdetail.first_name)
            NewGroupUser.save()   
                                        
            return NewGroup.pk           
        else:
            msg = "Must provide all required field."
            raise exceptions.ValidationError(msg)
        return data        

class AddGroupUserSerializer(serializers.Serializer):    
    GroupID = serializers.IntegerField()
    Mobilenumber = serializers.IntegerField()
    UserName = serializers.CharField()

    def validate(self,data):
        GroupID = data.get("GroupID", "")
        Mobilenumber = data.get("Mobilenumber", "")
        UserName = data.get("UserName", "")
        #user_id = self.context["user_id"]
        total = UserGroup.objects.get(id=GroupID).usercount
        Totalcount = GroupMember.objects.filter(UserGroup=GroupID).count()

        if total == Totalcount:
            msg = "Group Member count filled" 
            raise exceptions.ValidationError(msg)

        elif GroupMember.objects.filter(UserGroup=GroupID,Mobilenumber=Mobilenumber).exists():
            msg = "User alredy added in this group."
            raise exceptions.ValidationError(msg)
        elif GroupID and Mobilenumber:
            Group =  UserGroup.objects.get(id=GroupID)
            NewGroupUser =GroupMember(UserGroup=Group,Mobilenumber=Mobilenumber,UserName=UserName)
            NewGroupUser.save()                             
            return NewGroupUser.pk           
        else:
            msg = "Must provide all required field."
            raise exceptions.ValidationError(msg)
        return data 



class UserGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserGroup
        fields = [
            "id",
            "groupname",
            "startDate",
            "usercount",
            "createBy",
            "isActive",
            "AmountPerUser",
            "sarkriGhata",
            "groupbiddingtype"
        ]
  



