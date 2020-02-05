from django.db import models
from  django.contrib.auth.models import User,Group

# Create your models here.

class UserDetails(models.Model):   
    id = models.AutoField(primary_key=True)
    DateofBorth = models.DateField(max_length=30,null=True)
    AlternateMobileNumber=models.IntegerField(null=True)
    ProfilePic = models.URLField(max_length=200 ,null=True)


class UserGroup(models.Model):   
    id = models.AutoField(primary_key=True)
    groupname = models.TextField(max_length=30,null=True)
    startDate=models.DateField(max_length=12,null=True)
    usercount = models.IntegerField(null=True)
    createBy = models.IntegerField(null=True)
    isActive = models.IntegerField(null=True) 
    AmountPerUser = models.DecimalField(max_digits=8, decimal_places=2)
    sarkriGhata =  models.DecimalField(max_digits=8, decimal_places=2)
    groupbiddingtype = models.IntegerField()

class GroupMember(models.Model):   
    id = models.AutoField(primary_key=True)
    UserGroup= models.ForeignKey(UserGroup, on_delete=models.CASCADE)
    Mobilenumber = models.BigIntegerField() 
    UserName = models.TextField()


class GroupHistory(models.Model):   
    id = models.AutoField(primary_key=True)
    GroupMember= models.ForeignKey(GroupMember, on_delete=models.CASCADE)
    Mobilenumber = models.BigIntegerField() 
    UserName = models.TextField()
    ActualAmount = models.DecimalField(max_digits=8, decimal_places=2)
    AmountPaid = models.DecimalField(max_digits=8, decimal_places=2)
    AmountDue = models.DecimalField(max_digits=8, decimal_places=2)       
    startDate=models.DateField(max_length=12)


class GroupBidding(models.Model):   
    id = models.AutoField(primary_key=True)
    GroupMember= models.ForeignKey(GroupMember, on_delete=models.CASCADE)
    UserGroup= models.ForeignKey(UserGroup, on_delete=models.CASCADE)
    ActualAmount = models.DecimalField(max_digits=8, decimal_places=2) 
    biddingAmount =models.DecimalField(max_digits=8, decimal_places=2) 
    biddingBY = models.TextField()
    biddingbymobile=models.BigIntegerField()
    IsSelect = models.IntegerField()  
    Cyclenumber = models.IntegerField()  
    CreateDate=models.DateField(max_length=12)

class AmountRecived(models.Model):   
    id = models.AutoField(primary_key=True)
    UserGroup= models.ForeignKey(UserGroup, on_delete=models.CASCADE)
    ActualAmount = models.DecimalField(max_digits=8, decimal_places=2) 
    ActualRecived = models.DecimalField(max_digits=8, decimal_places=2) 
    Cyclenumber = models.IntegerField()
    RevicerName = models.TextField()
    Recivermobile =models.BigIntegerField() 
    RecivedDate=models.DateField(max_length=12)


class Biddingtype(models.Model):   
    id = models.AutoField(primary_key=True)
    Typename = models.TextField()
    TypeDescription =models.TextField()


