from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
#from quickstart.models import UserDetails,UserGroup
from quickstart.API.serializer import *
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from quickstart.models import *
from rest_framework.views import APIView
import datetime
from django.db.models import Q
from django.db.models.aggregates import Max


# Signup User 
@api_view(['POST'])
def RegisterUser(request):
    data=request.data
    serializer = RegisterSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data["user"]
    token, created = Token.objects.get_or_create(user=user)
    return Response({"token": token.key}, status=200)

#@login_required(login_url="/login/")
@api_view(['POST'])
def logout_user(request):
    data=request.data
    token = data['token']
    token_destroy = Token.objects.get(key=token)
    token_destroy.delete()
    logout(request)
    return  Response("User Logout Successfully")

# login user 
@api_view(['POST'])
def login_user(request):
    data=request.data
    #return Response(data)
    serializer = LoginSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data["user"]
    django_login(request, user)
    token, created = Token.objects.get_or_create(user=user)
    return Response({"token": token.key}, status=200)

# Create user Group 
class GroupUser(generics.GenericAPIView,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin):

    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserGroupSerializer
    queryset = UserGroup.objects.all()
    lookup_field = 'id'
    

    def get_queryset(self):
        return self.queryset.filter(createBy=self.request.user,isActive=1,groupStatus=5)

    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def perform_create(self, serializer):
        serializer.save(createBy=self.request.user)

    def put(self, request, id=None):
        return self.update(request, id)

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)        

    def delete(self, request, id=None):
        return self.destroy(request, id)

#Add Member to Group
@login_required(login_url="/login")
@api_view(['POST'])
def adduser_togroup(request):
    data=request.data
    token = data['token']
    userid = Token.objects.get(key=token).user_id
    serializer = AddGroupUserSerializer(data=data,context={'user_id':userid})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data)

@api_view(['get'])
def groupmember_list(request,id):
    data=request.data
    token = data['token']
    GroupMemberlist = GroupMember.objects.filter(UserGroup_id=id)
    serializer = GroupMemberSerializer(GroupMemberlist,many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def groupmember_update(request,id):
    data=request.data
    token = data['token']
    Mobilenumber = data['MobileNumber']
    UserName = data['UserName']
    status = UserGroup.objects.get(id__in=GroupMember.objects.filter(id=id).values('UserGroup_id')).groupStatus
    if status == 5:
        GroupMemberupdate =  GroupMember.objects.filter(id=id).update(Mobilenumber=Mobilenumber,UserName=UserName)
        GroupMemberlist = GroupMember.objects.filter(UserGroup_id__in =
                    GroupMember.objects.filter(id=id).values('UserGroup_id'))
        serializer = GroupMemberSerializer(GroupMemberlist,many=True)
        return Response(serializer.data)
    else:
        return Response("Group no longer in open state")

# # @login_required(login_url="/login") not use in class base type
# # @api_view(['PUT','GET'])
# class groupmember(APIView):
#     def get_object(self, id):
#         try:
#             return GroupMember.objects.get(id=id)
#         except GroupMember.DoesNotExist as e:
#             return Response( {"error": "Given groupmember object not found."}, status=404)

#     def get(self, request, id=None):
#         instance = self.get_object(id)
#         serailizer = GroupMemberSerializer(instance)
#         return Response(serailizer.data)

#     def put(self, request, id=None):
#         data = request.data
#         instance = self.get_object(id)
#         serializer = GroupMemberSerializer(instance, data=data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=200)
#         return Response(serializer.error, status=400)

#     def delete(self, request, id=None):
#         instance = self.get_object(id)
#         instance.delete()
#         return HttpResponse(status=204)

# #user bidding

# class StartGroupBidding(APIView):
#     def get_object(self, id):
#         try:
#             return GroupMember.objects.get(id=id)
#         except GroupMember.DoesNotExist as e:
#             return Response( {"error": "Given groupmember object not found."}, status=404)

#     def get(self, request, id=None):
#         instance = self.get_object(id)
#         serailizer = GroupMemberSerializer(instance)
#         return Response(serailizer.data)

#     def put(self, request, id=None):
#         data = request.data
#         instance = self.get_object(id)
#         serializer = GroupMemberSerializer(instance, data=data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=200)
#         return Response(serializer.error, status=400)
    
#     def post(self, request):
#         data = request.data
#         serializer = GroupMemberSerializer(data=data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=200)
#         return Response(serializer.error, status=400)

#     def delete(self, request, id=None):
#         instance = self.get_object(id)
#         instance.delete()
#         return HttpResponse(status=204)

# to start group group of first time insert bidding date concept 
@api_view(['PUT'])
def Group_Start(request,id = None):
    data=request.data
    token = data['token']
    userid = Token.objects.get(key=token).user_id
    GroupDetaildetails = UserGroup.objects.get(id=id,createBy = userid )
    if int(GroupDetaildetails.groupStatus) == 5 and int(GroupDetaildetails.biddingflag) == 0:
        UserGroup.objects.filter(id=id,createBy = userid ).update(groupStatus=5,biddingdate = datetime.datetime.today())
        Groupdetail = UserGroup.objects.get(id=id,createBy = userid )
        serializer = StatEndGroupUserSerializer(Groupdetail)
        return Response(serializer.data)   
    else:
        return Response(" User Group ALready Start") 



@api_view(['PUT'])
def Group_End(request,id = None):
    data=request.data
    token = data['token']
    userid = Token.objects.get(key=token).user_id
    GroupDetail = UserGroup.objects.filter(id=id,createBy = userid ).update(groupStatus=20,biddingflag = 0)
    Groupdetail = UserGroup.objects.get(id=id,createBy = userid )
    serializer = StatEndGroupUserSerializer(Groupdetail)
    return Response(serializer.data)

# terminate group if it is  in open state
@api_view(['PUT'])
def Group_Terminate(request,id = None):
    data=request.data
    token = data['token']
    userid = Token.objects.get(key=token).user_id
    status = UserGroup.objects.filter(id=id,createBy = userid ).values('groupStatus')
    if status == 5:
        GroupDetail = UserGroup.objects.filter(id=id,createBy = userid ).update(groupStatus=25)
        Groupdetail = UserGroup.objects.get(id=id,createBy = userid )
        serializer = StatEndGroupUserSerializer(Groupdetail)
        return Response(serializer.data)
    else:
        return Response("Group can't be termenated because it already in running state")

# get group list by group status got both group Admin and regular admin
@api_view(['GET'])
def Get_Group_ByStatus(request,status = None):
    data=request.data
    GroupDetail= {}
    token = data['token']
    if status is None:
        status = 10
    userid = Token.objects.get(key=token).user_id
    usermobilenumber = User.objects.get(id=userid).username
    GroupDetail = UserGroup.objects.filter(groupStatus=status,id__in =
                   GroupMember.objects.filter(Mobilenumber = usermobilenumber).values('UserGroup'))
    serializer = StatEndGroupUserSerializer(GroupDetail, many = True)
    return Response(serializer.data)


# let list of group for managing  this only fetch for admin only
@api_view(['GET'])
def Manage_Group_ByStatus(request,status = None):
    data=request.data
    GroupDetail= {}
    token = data['token']
    if status is None:
        status = 10
    userid = Token.objects.get(key=token).user_id
    GroupDetail = UserGroup.objects.filter(groupStatus=status, createBy = userid)
    serializer = StatEndGroupUserSerializer(GroupDetail, many = True)
    return Response(serializer.data)


@api_view(['GET'])
def Group_Bidding(request):
    data=request.data
    GroupDetail= {}
    token = data['token']
    userid = Token.objects.get(key=token).user_id
    GroupDetail = UserGroup.objects.filter(Q(biddingdate__isnull=True) | Q(biddingdate__lte = datetime.datetime.today())  ,
    Q(groupStatus=5) | Q(groupStatus = 15), createBy = userid )
    serializer = StatEndGroupUserSerializer(GroupDetail, many = True)
    return Response(serializer.data)


# only admin can activate group admin
@api_view(['PUT'])
def Start_Group_Bidding(request,id):
    if id is None:
        return Response("Group ID requried")    
    data=request.data
    GroupDetail= {}
    token = data['token']
    userid = Token.objects.get(key=token).user_id
    UserGroupDetails = UserGroup.objects.get(id=id)
    # check weather group biddings are still in progress or finished
    biddinggruopStatus = GroupBidding.objects.filter(UserGroup = UserGroupDetails).values('BiddingStatus')
    if len(biddinggruopStatus) == 0:
        groupbiddingstatus =5
    else:
       groupbiddingstatus = biddinggruopStatus[0]['BiddingStatus']
    if groupbiddingstatus != 10:
        biddingcycle = GroupBidding.objects.filter(UserGroup = UserGroupDetails).count()
        if biddingcycle == 0:
            GroupMemberlists = GroupMember.objects.filter(UserGroup = UserGroupDetails)
        else:
            GroupMemberlists = GroupMember.objects.filter(UserGroup = UserGroupDetails).exclude(
                                Mobilenumber__in = GroupBidding.objects.filter(UserGroup = UserGroupDetails,IsSelected =1
                                ).values('SelectedMobileNumber'))  
        insertgroupbidding = GroupBidding(UserGroup = UserGroupDetails,ActualAmount=UserGroupDetails.AmountPerUser,
                            Cyclenumber =(biddingcycle + 1),biddingAmount = 0,BiddingStatus=10)
        insertgroupbidding.save()
        
        for GroupMemberlist in GroupMemberlists:
            GroupBiddingEntriesdata = GroupBiddingEntries(GroupBidding =insertgroupbidding,selectedName =GroupMemberlist.UserName,
            SelectedMobileNumber = GroupMemberlist.Mobilenumber,Cyclenumber = (biddingcycle + 1))
            GroupBiddingEntriesdata.save()
        UserGroup.objects.get(id=id).update(biddgingCycle = (biddingcycle + 1))
        return Response("data save succefully")
    else:
        return Response("Previous bidding already in progres")


# fetch data for admin and single user of particular group
@api_view(['GET'])
def Group_Bidding_User_list(request,id):
    data=request.data
    GroupDetail= {}
    token = data['token']
    userid = Token.objects.get(key=token).user_id
    UserGroupDetails = UserGroup.objects.filter(id=id,createBy=userid)
    UserGroup_id = UserGroup.objects.get(id=id,createBy=userid)
    Groupbiddingdetails = GroupBidding.objects.filter(UserGroup = UserGroup_id,IsSelected =0)
    #userid = Token.objects.get(key=token).user_id
    if UserGroupDetails.count() == 1:        
        GroupBiddingEntriesdetails = GroupBiddingEntries.objects.filter(GroupBidding__in =Groupbiddingdetails,IsSelected =0)
    else:
        mobilenumber =User.objects.get(id=userid)
        GroupBiddingEntriesdetails = GroupBiddingEntries.objects.filter(GroupBidding__in =Groupbiddingdetails,IsSelected =0,
        SelectedMobileNumber  = int(mobilenumber.username) )

    serializer = GroupBiddingEntriesSerializer(GroupBiddingEntriesdetails, many = True)
    return Response(serializer.data)

# save bidding amount of group of individuals
@api_view(['PUT'])
def Save_Group_Bidding(request,id):
    data=request.data
    token = data['token']
    biddingAmount = data['BiddingAmount']
    UserMobileNumber = data['MobileNumber']
    GroupBiddingEntries.objects.filter(id=id,SelectedMobileNumber = UserMobileNumber).update(biddingAmount=biddingAmount)
    GroupBiddingEntriesdetails = GroupBiddingEntries.objects.filter(id=id,SelectedMobileNumber = UserMobileNumber)
    serializer = GroupBiddingEntriesSerializer(GroupBiddingEntriesdetails, many = True)
    return Response(serializer.data)


# Only Admin can select Bidding User
# update user group status to 15 ie bidding close or final
# id is groupbiddingentriesID 
@api_view(['PUT'])
def Select_Group_Bidding(request,id):
    data=request.data
    token = data['token']
    userid = Token.objects.get(key=token).user_id
    UserMobileNumber = data['MobileNumber']   
    # Get Select Bidding entries Details
    GroupBiddingEntriesdetails = GroupBiddingEntries.objects.get(id=id,SelectedMobileNumber = UserMobileNumber)
    biddingValue = GroupBiddingEntriesdetails.biddingAmount
    SelectedUserName = GroupBiddingEntriesdetails.selectedName
    if GroupBiddingEntriesdetails.IsSelected == 0:
        GroupBiddingDetails = GroupBidding.objects.get(id=GroupBiddingEntriesdetails.GroupBidding_id)
        GroupUserDetails = UserGroup.objects.get(id=GroupBiddingDetails.UserGroup_id)
        #cal Amount paid by per user 
        AmountPerUserPaid = int(biddingValue) / int(GroupUserDetails.usercount)
        
        GroupMemberlists = GroupMember.objects.filter(UserGroup = GroupUserDetails)
        
        for GroupMemberlist in GroupMemberlists:
                GroupHistorydata = GroupPaymentHistory(GroupBidding =GroupBiddingDetails,UserName =GroupMemberlist.UserName,
                Mobilenumber = GroupMemberlist.Mobilenumber,Cyclenumber = GroupBiddingDetails.Cyclenumber,
                ActualAmount =AmountPerUserPaid)
                GroupHistorydata.save()
        GroupBiddingEntries.objects.filter(id=id,SelectedMobileNumber = UserMobileNumber).update(IsSelected=1)
    
        GroupBidding.objects.filter(id=GroupBiddingEntriesdetails.GroupBidding_id).update(biddingAmount=biddingValue,selectedName=SelectedUserName,SelectedMobileNumber = UserMobileNumber,IsSelected=1)
        return Response("User Selected Successfully")
    else:
        return Response("User Already Selected")



@api_view(['GET'])
def Group_Payment_User_list(request,id):
    data=request.data
    GroupDetail= {}
    token = data['token']
    userid = Token.objects.get(key=token).user_id  
    CheckgroupAdmin  = UserGroup.objects.filter(id=id,createBy=userid)  
    UserGroupDetails = UserGroup.objects.get(id=id)   
    biddingcycle = GroupBidding.objects.filter(UserGroup = UserGroupDetails).count()    
    groupbiddingdetails = GroupBidding.objects.filter(UserGroup = UserGroupDetails,Cyclenumber=int(biddingcycle))[0]

    
    if CheckgroupAdmin.count() == 1:
        GroupPaymentHistorydetails = GroupPaymentHistory.objects.filter(GroupBidding = groupbiddingdetails)
        serializer = GroupPaymentHistorySerializer(GroupPaymentHistorydetails, many = True)
       
    else:
        mobilenumber =User.objects.get(id=userid)
        GroupPaymentHistorydetails = GroupPaymentHistory.objects.filter(GroupBidding = groupbiddingdetails,
        Mobilenumber  = int(mobilenumber.username) )
        serializer = GroupPaymentHistorySerializer(GroupPaymentHistorydetails, many = True)
    return Response(serializer.data)


@api_view(['PUT'])
def Group_Payments(request,id):
    data=request.data
    token = data['token']
    PaidAmount = data['AmountPaid']
    UserMobileNumber = data['Mobilenumber']
    GroupPaymentHistorydetails = GroupPaymentHistory.objects.filter(id=id,Mobilenumber = UserMobileNumber)[0]
    totalAmountDue = int(GroupPaymentHistorydetails.ActualAmount) - int(PaidAmount)
    GroupPaymentHistory.objects.filter(GroupBidding_id=id,Mobilenumber = UserMobileNumber).update(AmountPaid=PaidAmount,AmountDue=totalAmountDue)
    return Response("Payemts successfully")


@api_view(['PUT'])
def Send_Amount(request,id):
    data=request.data
    token = data['token']
    userid = Token.objects.get(key=token).user_id  
    CheckgroupAdmin  = UserGroup.objects.filter(id=id,createBy=userid) 
    if CheckgroupAdmin.count() == 1:
        UserGroupDetails=  UserGroup.objects.get(id=id,createBy=userid)
        biddingcycle = GroupBidding.objects.filter(UserGroup = UserGroupDetails).count()  
           
        groupbiddingDetail = GroupBidding.objects.filter(UserGroup = UserGroupDetails,Cyclenumber=biddingcycle)[0]
        
        Amountdetails = AmountRecived(UserGroup = UserGroupDetails,ActualAmount= groupbiddingDetail.biddingAmount ,ActualRecived= groupbiddingDetail.biddingAmount ,
                        Cyclenumber = biddingcycle,RevicerName = groupbiddingDetail.selectedName,
                        Recivermobile =groupbiddingDetail.SelectedMobileNumber ,RecivedDate= datetime.datetime.today())
        Amountdetails.save()
        GroupBidding.objects.filter(UserGroup = UserGroupDetails,Cyclenumber=biddingcycle).update(BiddingStatus=15)
        return Response("Payemts successfully")
    else:
        return Response("You dont have permission to send amount")



@api_view(['Put'])
def update_user_details(request):
    data = request.data
    token = data['token']
    AlternateMobileNumber = data['AlternateMobileNumber']
    ProfilePic = data['ProfilePic']
    DateofBirth = data['DateofBirth']
   
    userid = Token.objects.get(key=token).user_id
    UserDetails.objects.filter(User_id=userid).update(ProfilePic=ProfilePic,AlternateMobileNumber=AlternateMobileNumber,DateofBirth=DateofBirth)
    UserDetailsupdate = UserDetails.objects.get(User_id=userid)
    serializer = UserDetailsSerializer(UserDetailsupdate)
    return Response(serializer.data)


# user group data crud
class UserProfile(generics.GenericAPIView,
                    mixins.ListModelMixin):

    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = User.objects.all()
    #queryset = User.objects.select_related('UserDetails').get(id=5)
    lookup_field = 'id'    

    def get_queryset(self):
        return self.queryset.filter(username=self.request.user)

    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)


