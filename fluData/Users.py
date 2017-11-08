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
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from . import models


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
        if request.method == "POST" :

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

    @login_required(login_url="login")
    def mainv(request):
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

def GetUserProfile(request):
    # tUser=models.Person.objects.get(pName = request.user.username)
    # proDict={
    #     "name":tUser.pName,
    #     "id":tUser.pID,
    #     "phone":tUser.pPhone,
    #     "type":tUser.pType,
    # # }
    request.session["profile"] = request.user.userprofile.get_profile_dict()

def get_normal_context(request):
    ndict = {
        "user":{
            "profile":""
            }
            }
    return ndict

@login_required(login_url = "login")
def mainv(request):
    tcontext = get_normal_context(request)
    return render(request, "main.html", tcontext)
    
    

@require_http_methods(["GET", "POST"])
def loginv(request):
    # login_error={""}
    if request.user.is_authenticated():
        return HttpResponseRedirect('/user/main')
    if request.method == "GET":
        return render(request,"login.html")
    if request.method == "POST":
        if not ( ("username" in request.POST) and ("password" in request.POST) ):
            return render(request,"login.html",{"login_error":["用户名或密码不能为空"]})
        user_res=authenticate(username=request.POST["username"],password=request.POST["password"])
        if user_res and (user_res.is_active):
            auth.login(request,user_res)
            return HttpResponseRedirect("/user/loading/")
        else:
            return render(request,"login.html",{"login_error":["密码或用户名有误，请重试"]})
    return render(request,"login.html")

def loadingv(request):
    # GetUserProfile(request)
    return HttpResponseRedirect("/user/main/")

@login_required(login_url = "login")
def housev(request):
    if request.method == "GET":#读取资源
        alls = models.House.objects.all()
        contexts = {"house":{"about":[]}}
        for i in alls:
            contexts["house"]["about"].append(i.get_house_about())
        return render(request, "house.html", contexts)
    return render(request, "error.html")

@login_required(login_url = "login")
def add_house(request):
    if request.method == "GET":
        return render(request, "add_house.html")
    elif request.method == "POST":
        # print(request.POST["name"])
        new_house = models.House(
            name=request.POST["name"],
            phone=request.POST["phone"],
            price=request.POST["price"],
            price_unit=request.POST["price_unit"],
            house_type=request.POST["house_type"],
            ikeys=request.POST["ikeys"],
            community=request.POST["community"],
            position=request.POST["position"],
            area=request.POST["area"],
            kind=request.POST["kind"],
            more=request.POST["more"],
            belong=request.user.userprofile.id,
            decor=request.POST["decor"],
            level=request.user.userprofile.level,
            status=request.POST["status"],
            floor=request.POST["floor"]
        )
        new_house.save()
        print(new_house.name)
        return render(request, "add_success.html")
    return render(request, "error.html")

@login_required(login_url = "login")
def detail_house(request):
    if request.method == "GET":
        t_id = int(request.GET["id"])
        t_src = models.House.objects.get(id = t_id)
        return render(request, "detail_house.html", {"house":{"detail":t_src.get_house_detail()}})
    return render(request, "error.html")

@login_required(login_url = "login")
def alter_house(request):
    if request.method == "GET":
        t_id = int(request.GET["id"])
        t_src = models.House.objects.get(id = t_id)
        return render(request, "alter_house.html", {"house":{"detail":t_src.get_house_detail}})
    elif request.method == "POST":
        t_id = int(request.GET["id"])
        t_src = models.House.objects.get(id = t_id)
        t_alter = request.GET["alter_house"]
        # for i in t_alter:
            # t_src.update(str())
        # t_src.update()
    return render(request, "error.html")

@login_required(login_url = "login")
def find_house(request):
    return render(request,"error.html")

userv=UserViews()

houseUrls=[
    url(r"^$",housev,name="house"),
    url(r"^add/",add_house,name="add_house"),
    url(r"^find/",find_house,name="find_house"),
    url(r"^alter/",alter_house,name="alter_house"),
    url(r"^detail/",detail_house,name="detail_house"),
]

mainUrls=[

]



userUrls=[
    url(r"^$",mainv,name="main"),
    url(r"^main/",mainv,name="main"),
    url(r"^house/",include(houseUrls)),
    url(r"^client/",userv.clientv,name="client"),
    url(r"^achievement/",userv.achievementv,name="achievement"),
    url(r"^not_permitted/",TemplateView.as_view(template_name="permission_denied.html"),name="PermissionDenied"),
    url(r"^login/",loginv,name="login"),
    url(r"^logout/",userv.logoutv,name="logout"),
    url(r"^api/",userv.apiv,name="api"),
    url(r"^manage/",userv.managev,name="manage"),
    url(r"^loading/" , loadingv , name = "loading"),
]