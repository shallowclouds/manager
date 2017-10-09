#coding=UTF-8

from django.db import models


class tHouse(models.Model):
    tID=models.AutoField(u"房源ID",primary_key=True)
    tName=models.CharField(u"客户姓名",max_length=200,null=True)
    tPhone=models.CharField(u"客户电话",max_length=100,null=True)
    tPrice=models.CharField(u"价格",max_length=100,null=True)
    tCommunity=models.CharField(u"小区",max_length=100,null=True)
    tPos=models.CharField(u"位置",max_length=100,null=True)
    tArea=models.CharField(u"面积",max_length=100,null=True)
    tType=models.CharField(u"户型",max_length=100,null=True)
    tOther=models.CharField(u"备注",max_length=1000,null=True)

    def __str__(self):
        return self.tName


class Person(models.Model):
    pName=models.CharField(u"用户名",max_length=20)
    pID=models.AutoField(u"用户ID",primary_key=True)
    pType=models.IntegerField(u"用户权限",default=3)
    # pHead=models.ForeignKey("Pictures",blank=True,null=True)
    pEmail=models.EmailField(u"邮箱地址",blank=True,null=True)
    pPassword=models.CharField(u"密码",max_length=500,null=True)
    pPhone=models.CharField(u"手机号码",max_length=30,null=True)
    pLastLogin=models.DateField(u"上次登录时间",blank=True,null=True)

    def __str__(self):
        return self.pName


# class Client(models.Model):
#     cID=models.AutoField(u"客户ID",primary_key=True)
#     cName=models.CharField(u"姓名",max_length=30,null=True)
#     cPhone=models.CharField(u"手机号码",max_length=30,null=True)
#     cDetail=models.CharField(u"备注",max_length=300,default="",blank=True,null=True)
#     cBelong=models.ForeignKey("Person",null=True)
#
#     def __str__(self):
#         return self.cName
#
#
# class House(models.Model):
#     hID=models.AutoField(u"房屋ID",primary_key=True)
#     hType=models.IntegerField(u"权限级别",default=3)
#     hClient=models.ForeignKey("Client")
#     hBelong=models.ForeignKey("Person")
#     hDetail=models.CharField(u"备注",max_length=300,default="",blank=True)
#     hPosition=models.CharField(u"地址",max_length=50)
#     hArea=models.IntegerField(u"面积")
#     hFloor=models.IntegerField(u"楼层")
#     hLowPrice=models.IntegerField(u"最低价格")
#     hPrice=models.IntegerField(u"建议价格",blank=True)
#     hDecoration=models.CharField(u"装修类型",max_length=100,blank=True)
#     hHouseType=models.CharField(u"房屋类型",max_length=100,blank=True)
#     hCount=models.CharField(u"厅室数量",max_length=100,blank=True)
#     hDate=models.DateField(u"记录时间")
#
#     def __str__(self):
#         return str(self.hID)
#
#
# class Pictures(models.Model):
#     iID=models.AutoField(u"图片ID",primary_key=True)
#     iPath=models.CharField(u"图片路径",max_length=300)
#     # iUpFrom=models.ForeignKey("Person")
#
#     def __str__(self):
#         return self.iPath
#
#
# class Community(models.Model):
#     cID=models.AutoField(u"小区ID",primary_key=True)
#     cAddress=models.CharField(u"小区地址",max_length=200)
#     cName=models.CharField(u"小区名字",max_length=200)
#
#     def __str__(self):
#         return self.cName
#
#
# class Buier(models.Model):
#     bID=models.AutoField(u"买家ID",primary_key=True)
#     bName=models.CharField(u"买家姓名",max_length=20)
#     bPhone=models.CharField(u"买家电话",max_length=30)
#     bDetail=models.CharField(u"备注",max_length=300,blank=True)
#     bCount=models.CharField(u"厅室数量",max_length=30,blank=True)
#     bPrice=models.IntegerField(u"价格",blank=True)
#     bCommunity=models.ForeignKey("Community",blank=True)
#
#     def __str__(self):
#         return self.bName







