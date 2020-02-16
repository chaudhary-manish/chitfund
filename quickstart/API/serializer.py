from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from quickstart.models import UserDetails,GroupMember
from django.contrib.auth.models import User
from rest_framework import exceptions


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

class EmployeeSerializer(serializers.ModelSerializer):
    #profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'first_name',
                'last_name', 'email']



class UserDetailsSerializers(serializers.ModelSerializer):
    class Meta:
        model =UserDetails
        fields = ['id', 'groupname', 'startDate', 'usercount',
         'createBy', 'isActive','AmountPerUser','sarkriGhata','groupbiddingtype']


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model= GroupMember
        fields =['UserGroup',
        'UserName',
        'Mobilenumber'
        ]
