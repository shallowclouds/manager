#coding=UTF-8
from django.conf.urls import include,url
from django.http import HttpResponse
# from django.template import context
from django.shortcuts import render
from django.template import Template, Context
from django.template.loader import get_template
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView
# from . import views
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth import authenticate
from . import models
import json


def syncUsersToAdmin():
    userres=auth.models.User.objects.all()
    # print(models.Person.objects.filter(pName="123").count())
    for i in userres:
        tres=models.Person.objects.filter(pName=i.username)
        if tres.count()==0:
            tPerson=models.Person(pName=i.username,pPassword="null",pPhone="null")
            tPerson.save()


class UserViews(object):

    def __init__(self):
        pass

    def loginv(self,request):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/user/main')
        if request.method == "GET":
            return render(request,"login.html")
        if request.method == "POST":
            if not ( ("username" in request.POST) and ("password" in request.POST)):
                return render(request,"login.html",{"login_error":["用户名或密码不能为空"]})
            user_res=authenticate(username=request.POST["username"],password=request.POST["password"])
            if user_res and (user_res.is_active):
                auth.login(request,user_res)
                return HttpResponseRedirect("/user/main")
            else:
                return render(request,"login.html",{"login_error":["密码或用户名有误，请重试"]})
        return render(request,"login.html")

    def housev(self,request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect("/user/login/")
        if request.method=="GET":
            results=models.tHouse.objects.all()
            tcontext={"house":[],"user":{"name":request.user.username}}
            for i in results:
                tcontext["house"].append({
                    "ID":i.tID,
                    "name":i.tName,
                    "community":i.tCommunity,
                    "phone":i.tPhone,
                    "price":i.tPrice,
                    "area":i.tArea,
                    "pos":i.tPos,
                    "type":i.tType,
                    "other":i.tOther
                })
            # print(tcontext["house"][0])
            return render(request,"house.html",context=tcontext)
        if request.method=="POST":

            return render(request,"house.html")

    def add_housev(self,request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect("/user/login/")
        if request.method=="GET":
            return render(request,"add_house.html",context={"user":{"name":request.user.username}})
        if request.method=="POST":
            res_json={"res":True}
            new_house=models.tHouse(tName=request.POST["name"],
                                    tCommunity=request.POST["community"],
                                    tPhone=request.POST["phone"],
                                    tPrice=request.POST["price"],
                                    tArea=request.POST["area"],
                                    tPos=request.POST["pos"],
                                    tType=request.POST["type"],
                                    tOther=request.POST["other"]
                                    )
            new_house.save()
            return HttpResponse(json.dumps(res_json),content_type="application/json")

    def find_housev(self,request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect("/user/login/")
        if request.method=="GET":
            return render(request,"find_house.html",context={"user":{"name":request.user.username}})
        if request.method=="POST":
            finds=request.POST["keyword[]"]
            sfind=finds.split(" ")
            ours=models.tHouse.objects.all()
            results={"res":[]}
            for i in ours:
                flag=False
                # print(sfind)
                for j in sfind:
                    # print(j)
                    if (j in i.tName) or (j in i.tType) or (j in i.tOther) or (j in i.tPos) or (j in i.tArea) or (j in i.tPhone) or (j in i.tCommunity) or (j in i.tPrice):
                        continue
                    else:
                        flag=True
                        print(j,i)
                        break
                if not flag:
                    results["res"].append({
                    "ID":i.tID,
                    "name":i.tName,
                    "community":i.tCommunity,
                    "phone":i.tPhone,
                    "price":i.tPrice,
                    "area":i.tArea,
                    "pos":i.tPos,
                    "type":i.tType,
                    "other":i.tOther
                })
        return HttpResponse(json.dumps(results), content_type="application/json")

    def alter_housev(self,request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect("/user/login/")
        if request.method=="GET":
            return render(request,"detail_house.html",context={"user":{"name":request.user.username}})

    def get_context(self,objs):
        res={}
        print(objs)
        print("2333")
        res={"ID":objs.tID,
                    "name":objs.tName,
                    "community":objs.tCommunity,
                    "phone":objs.tPhone,
                    "price":objs.tPrice,
                    "area":objs.tArea,
                    "pos":objs.tPos,
                    "type":objs.tType,
                    "other":objs.tOther
             }
        return res

    def detail_housev(self,request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect("/user/login/")
        if request.method=="GET" and not("id" in request.GET):
            return render(request,"detail_house.html",context={"user":{"name":request.user.username}})
        elif request.method=="GET":
            tcontext={"detail_house":self.get_context(models.tHouse.objects.filter(tID=int(request.GET["id"]))[0]),"user":{"name":request.user.username}}
            return render(request,"detail_house.html",context=tcontext)


    def clientv(self,request):
        if request.user.is_authenticated():
            return render(request,"client.html")
        return HttpResponseRedirect("/user/login/")

    def achievemenvt(self,request):
        if request.user.is_authenticated():
            return render(request,"achievement.html")
        return HttpResponseRedirect("/user/login/")

    def mainv(self,request):
        syncUsersToAdmin()
        if request.user.is_authenticated():
            tmpuser=models.Person.objects.filter(pName=request.user.username)
            tcontext={}
            tcontext={"user":{"name":tmpuser[0].pName,"profile":["用户名："+tmpuser[0].pName,"电话号码："+tmpuser[0].pPhone]}}
            return render(request,"main.html",context=tcontext)
        return HttpResponseRedirect("/user/login/")

    def apiv(self,request):
        return render(request, "error.html", {"error": {"title": "正在建设中=-=", "detail": "该页面正在建设中=-=，详情请联系管理员"}})

    def achievementv(self,request):
        return render(request, "error.html", {"error": {"title": "正在建设中=-=", "detail": "该页面正在建设中=-=，详情请联系管理员"}})

    def logoutv(self,request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/user/login/")
        if request.method=="GET":
            auth.logout(request)
            return HttpResponseRedirect("/user/login/")
        return render(request, "error.html", {"error": {"title": "正在建设中=-=", "detail": "该页面正在建设中=-=，详情请联系管理员"}})


    def managev(self,request):
        if request.user.is_authenticated():
            return render(request, "error.html", {"error": {"title": "正在建设中=-=", "detail": "该页面正在建设中=-=，详情请联系管理员"}})
        return HttpResponseRedirect("/user/login/")

    def testv(self,request):
        return render(request,"test.html")






# userUrls=[
#     url(r"^main/",CView.get(name="main"),name="main"),
#     url(r"^house/",views.User_Views.get(name="house"),name="house"),
#     url(r"^client/",views.User_Views.get(name="client"),name="client"),
#     url(r"^achievement/",views.User_Views.get(name="achievement"),name="achievement"),
#     url(r"^profile/",views.User_Views.get(name="profile"),name="profile"),
#     url(r"^not_permitted",TemplateView.as_view(template_name="user/permission_denied.html"),name="PermissionDenied"),
#     url(r"^login/",views.login),
#     url(r"^logout/",views.logout),
#     url(r"^api/",include(apiUrls)),
# ]
userv=UserViews()

houseUrls=[
    url(r"^$",userv.housev,name="house"),
    url(r"^add/",userv.add_housev,name="add_house"),
    url(r"^find/",userv.find_housev,name="find_house"),
    url(r"^alter/",userv.alter_housev,name="alter_house"),
    url(r"^detail",userv.detail_housev,name="detail_house"),
]

mainUrls=[

]


userUrls=[
    url(r"^$",userv.mainv,name="main"),
    url(r"^main/",userv.mainv,name="main"),
    url(r"^house/",include(houseUrls)),
    url(r"^client/",userv.clientv,name="client"),
    url(r"^achievement/",userv.achievementv,name="achievement"),
    url(r"^not_permitted/",TemplateView.as_view(template_name="permission_denied.html"),name="PermissionDenied"),
    url(r"^login/",userv.loginv,name="login"),
    url(r"^logout/",userv.logoutv,name="logout"),
    url(r"^api/",userv.apiv,name="api"),
    url(r"^manage/",userv.managev,name="manage"),
]