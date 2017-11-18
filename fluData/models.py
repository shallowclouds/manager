#coding=UTF-8

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import time



class House(models.Model):
    PRICE_CHOICES = (
        ('万元',"万元"),
        ('千元',"千元"),
        ('百元',"百元"),
        ('  元',"元"),
    )
    SELL = "出售"
    RENT = "出租"
    TYPE_CHOICES = (
        (SELL,"SELL"),
        (RENT,"RENT"),
    )

    DECOR_CHOICES = (
        ("清水","清水"),
        ("简装","简装"),
        ("中装","中装"),
        ("精装","精装"),
        ("豪装","豪装"),
        ("暂无","暂无"),
    )

    STATUS_CHOICES = (
        ("交易完成","该交易已在本店完成"),
        ("失效","该房源已失效（已出售或出租）"),
        ("有效","该房源有效"),
    )

    id = models.AutoField(u"id", primary_key = True)
    name = models.CharField(u"客户姓名", max_length = 30, null = True, blank = True)
    phone = models.CharField(u"手机号码", max_length = 20, null = True, blank = True, default = "暂无")

    price = models.IntegerField(u"售价", null = True, default = 0)
    price_unit = models.CharField(u"售价单位", max_length = 20, choices = PRICE_CHOICES, null = True, default = "万元", blank = True)
    
    house_type = models.CharField(u"类型", max_length = 20, null = True, choices = TYPE_CHOICES, default = SELL, blank = True)

    ikeys = models.CharField(u"钥匙位置", max_length = 40, null = True, default = "暂无", blank = True)
    community = models.CharField(u"社区", max_length = 50,null = True, default = "暂无", blank = True)
    position = models.CharField(u"地址", max_length = 200, null = True, default = "暂无", blank = True)
    area = models.IntegerField(u"面积", null = True, default = 0)
    kind = models.CharField(u"户型", max_length = 50, null = True, default = "暂无", blank = True)
    more = models.CharField(u"备注", max_length = 1000, null = True, default = "暂无", blank = True)
    floor = models.IntegerField(u"楼层", null = True, default = 0, blank=True)
    level = models.IntegerField(u"等级", null = True, default = 3)

    status = models.CharField(u"资源状态", max_length = 20, null = True, choices = STATUS_CHOICES, default = "有效", blank = True)
    
    decor = models.CharField(u"装修情况", max_length = 50, null = True, choices = DECOR_CHOICES, default = "暂无", blank = True)

    belong = models.IntegerField(u"所有者", null = True, default = 1)

    all_things = models.TextField(u"搜索信息", null = True, default = "暂无", blank = True)
# 
    change_time = models.DateTimeField(u"上次修改时间", blank = True, default = timezone.now, null = True)

    def __str__(self):
        return self.name

    def get_house_detail(self):
        try:
            t_belong = UserProfile.objects.get(id=self.id).name
        except:
            t_belong = self.id

        try:
            last_change = self.change_time.strftime("%y-%m-%d %X")
        except:
            last_change = "无"
        details = {
            "id" : self.id,
            "name" : self.name,
            "phone" : self.phone,
            "price" : self.price,
            "price_unit" : self.price_unit,
            "house_type" : self.house_type,
            "ikeys" : self.ikeys,
            "community" : self.community,
            "position" : self.position,
            "area" : self.area,
            "kind" : self.kind,
            "more" : self.more,
            "belong" : t_belong,
            "decor" : self.decor,
            "level" : self.level,
            "status" : self.status,
            "floor" : self.floor,
            "last_change" : last_change,
        }
        return details

    def get_refresh_data(self):
        details = {
            "id" : self.id,
            "name" : self.name,
            "phone" : self.phone,
            "price" : str(self.price)+self.price_unit,
            "house_type" : self.house_type,
            "ikeys" : self.ikeys,
            "community" : self.community,
            "position" : self.position,
            "area" : self.area,
            "kind" : self.kind,
            "more" : self.more,
            "belong" : self.belong,
            "decor" : self.decor,
            "level" : self.level,
            "status" : self.status,
            "floor" : self.floor,
        }
        return details

    def get_house_about(self):
        about = {
            "id" : self.id,
            "phone" : self.phone,
            "position" : self.position,
            "name" : self.name,
            "area" : self.area,
            "decor" : self.decor,
            "kind" : self.kind,
            "floor" : self.floor,
            "price" : self.price,
            "price_unit" : self.price_unit,
            "community" : self.community,
        }
        return about

    def refresh(self):
        contents = self.get_house_detail()
        strs = ""
        for i in contents.values:
            strs.join(str(i))
        self.all_things = strs


class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(u"姓名", max_length=20, blank = True)
    id = models.AutoField(u"ID", primary_key = True)
    level = models.IntegerField(u"用户等级", default = 3)
    phone = models.CharField(u"手机号码", max_length = 20, null = True, blank = True)
    lastCheck = models.DateTimeField(u"上次签到时间", blank = True, null= True, default=timezone.now)
    

    def __str__(self):
        return self.name

    def get_profile_dict(self):
        proDict = {
            "name" : self.name,
            "id" :  self.id,
            "level" : self.level,
            "phone" : self.phone,
            "last_check" : self.lastCheck.strftime("%y-%m-%d %X"),
            "username" : self.user.username,
        }
        return proDict







