#coding=UTF-8
from django.conf.urls import include,url
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# from django.template import context
from django.shortcuts import render
from django.template import Template, Context
from django.template.loader import get_template
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
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone
from django.views import View
import datetime
import logging as log

class test_view(View):

    def get(self, request, *args, **kwargs):
        dicts= {"test":{"time":request.user.userprofile.lastCheck.strftime("%y-%m-%d")}}
        return render(request, "user/test.html", dicts)

# @method_decorator(login_required, name="get", login_url="login")
class main_view(View):

    def get_chk_time(self):
        return timezone.now().strftime("%y-%m-%d")

    @method_decorator(login_required(login_url="login"))
    def get(self, request, *args, **kwargs):
        usrpro = {}
        try:
            usrpro["user"] = request.user.userprofile.get_profile_dict()
        except Exception as e:
            print(e)
            usrpro={}
        return render(request, "user/main.html", usrpro)

    @method_decorator(login_required(login_url="login"))
    def post(self, request, *args, **kwargs):
        lst_chk = request.user.userprofile.lastCheck.strftime("%y-%m-%d")
        now_chk = self.get_chk_time()
        # print(now_chk)
        # print(lst_chk)
        if lst_chk != now_chk:
            request.user.userprofile.lastCheck=timezone.now()
            request.user.userprofile.save()
            log.info("check:"+str(request.user.username)+" "+now_chk)
            return JsonResponse({"res":"签到成功！", "is":True})
        else:
            return JsonResponse({"res":"签到失败，您已签到或未登录。","is":False})



# @method_decorator(login_required, name="get", login_url="login")
class house_view(View):

    @method_decorator(login_required(login_url="login"))
    def get(self, request, *args, **kwargs):
        res = models.House.objects.all().order_by("change_time","id")[:10]
        dicts = {"house":{"about":[]}}
        for i in res:
            dicts["house"]["about"].append(i.get_house_about())
        return render(request, "user/house.html", dicts)


    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return JsonResponse({"error":"您没有登录，请登录再试。"})
        finds = json.loads(request.POST["data"])
        # print(finds)
        res = models.House.objects.all().order_by("id").filter(all_things__contains=finds["0"])
        for i in finds.values():
            res = res.filter(all_things__contains=str(i))
        dicts = []
        for i in res:
            dicts.append(i.get_house_about())
        return JsonResponse(dicts, safe=False)
            


class house_add_view(View):

    @method_decorator(login_required(login_url="login"))
    def get(self, request, *args, **kwargs):
        return render(request, "user/house_add.html")

    @method_decorator(login_required(login_url="login"))
    def post(self, request, *args, **kwargs):
        t_house={}
        for i in request.POST:
            if not("csrfmiddlewaretoken" in i):
                t_house[i]=request.POST[i]
        if t_house["floor"]=="":
            t_house["floor"]=0
        t_house["belong"]=request.user.userprofile.id
        tt_house=models.House(**t_house)
        tt_house.save()
        return render(request, "user/house_add_success.html")



class manage_view(View):
    
    @method_decorator(login_required(login_url="login"))
    def get(self, request, *args, **kwargs):
        if request.user.userprofile.level>1:
            return render(request, "user/error.html", {"error":{"title":"访问被拒绝","content":"您不是管理员，因此无法访问此页面。"}})
        objs = models.UserProfile.objects.all()
        contexts = {"users":[]}
        for i in objs:
            # print(i)
            contexts["users"].append(i.get_profile_dict())
        return render(request, "user/manage.html" , contexts)



class login_view(View):
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse("main"))
        return render(request, "user/login.html")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse("main"))
        if "username" in request.POST and "password" in request.POST:
            user_res = authenticate(username=request.POST["username"], password=request.POST["password"])
            if user_res and user_res.is_active:
                auth.login(request, user_res)
                return HttpResponseRedirect("/user/main/")
            else:
                return render(request, "user/login.html", {"login_error":["密码或用户名有误，请检查输入后重试"]})
        else:
            return render(request, "user/login.html", {"login_error":["用户名或密码不能为空"]})
        return render(request, "user/login.html")

@login_required(login_url = "login")
def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("login"))

def index(request):
    return render(request, "index.html")

class house_alter_view(View):

    @method_decorator(login_required(login_url="login"))
    def get(self, request, *args, **kwargs):
        if not ("id" in request.GET):
            return render(request, "user/error.html",{"error":{"title":"房源不存在", "content":"该房源不存在！请刷新数据。"}})
        context=models.House.objects.get(id=request.GET["id"]).get_house_detail()
        return render(request, "user/house_alter.html",context)
    
    @method_decorator(login_required(login_url="login"))
    def post(self, request, *args, **kwargs):
        for i in request.POST:
            t_house={}
        for i in request.POST:
            print(i)
            if not(("csrfmiddlewaretoken") in i or ("id" in i)):
                t_house[i]=request.POST[i]
        if t_house["floor"]=="":
            t_house["floor"]=0
        tt_house=models.House.objects.filter(id=request.POST["id"])
        tt_house.update(**t_house)
        return render(request, "user/house_add_success.html")


class house_detail_view(View):

    @method_decorator(login_required(login_url="login"))
    def get(self, request, *args, **kwargs):
        if not ("id" in request.GET):
            return HttpResponse("error")
        obj = get_object_or_404(models.House, id=request.GET["id"])
        if obj.level<request.user.userprofile.level:
            return render(request, "user/error.html", {"error":{"title":"访问被拒绝","content":"对于该房源的访问被拒绝，可能是您的权限不够，请联系管理员。"}})
        context = {"house":{"detail":obj.get_house_detail()}}
        return render(request, "user/house_detail.html", context)

@login_required(login_url="login")
def refresh_view(request):
    objs = models.House.objects.all()
    for i in objs:
        contents = i.get_house_detail()
        strs = ""
        for j in contents.values():
            strs+=(str(j))
        print(strs)
        i.all_things = strs
        i.save()
    return JsonResponse({"info":"ok"})

class user_add(View):
    
    @method_decorator(login_required(login_url="login"))
    def get(self, request, *args, **kwargs):
        return render(request, "user/user_add.html")

    @method_decorator(login_required(login_url="login"))
    def post(self, request, *args, **kwargs):
        try:
            usr_dict = {"password":request.POST["password"], "email":request.POST["email"]}
            usr = User.objects.create_user(request.POST["username"], **usr_dict)
            usr.save()
            usrpro_dict = {"name":request.POST["name"], "phone":request.POST["phone"], "level":request.POST["level"], "user":usr}
            usrpro = models.UserProfile(**usrpro_dict)
            usrpro.save()
        except Exception as e:
            print(e)
            return render(request, "user/error.html", {"error":{"title":"保存错误！", "content":"emmmm似乎发生了什么出乎意料的错误，请联系开发者解决问题。。"}})
        # usrpro = models.UserProfile.objects.create(name=request.POST["name"], user=usr, phone=request.POST["phone"])
        return render(request, "user/add_success.html")

main_urls = [
    url(r"^$", main_view.as_view(), name="main"),
    # url(r"^main/", main_view.as_view(), name="main"),
]

houses_urls = [
    url(r"^$", house_view.as_view(), name="house"),
    url(r"^add/", house_add_view.as_view(), name="house/add"),
    url(r"^detail/", house_detail_view.as_view(), name="house/detail"),
    url(r"^alter/", house_alter_view.as_view(), name="house/alter"),
]

manage_urls = [
    url(r"^$", manage_view.as_view(), name="manage"),
    # url(r"^adduser/")
]

auth_urls = [
    url(r"^login/", login_view.as_view(), name="login"),
    url(r"^logout/", logout_view, name="logout"),
    url(r"^add/",user_add.as_view(), name="auth/add"),
]

help_urls = [

]

api_urls = [
    url(r"refresh/", refresh_view, name="api/refresh"),
]

urls = [
    url(r"^main/", include(main_urls)),
    url(r"^house/", include(houses_urls)),
    url(r"^manage/", include(manage_urls)),
    url(r"^help/", include(help_urls)),
    url(r"^auth/", include(auth_urls)),
    url(r"^api/", include(api_urls)),
]
