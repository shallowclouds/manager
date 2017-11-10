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

from django.views import View

class test_view(View):

    def get(self, request, *args, **kwargs):
        return render(request, "user/test.html")

class main_view(View):

    def get(self, request, *args, **kwargs):
        return render(request, "user/main.html")

class house_view(View):

    def get(self, request, *args, **kwargs):
        return render(request, "user/house.html")

class house_add_view(View):

    def get(self, request, *args, **kwargs):
        return render(request, "user/add_house.html")

class manage_view(View):

    def get(self, request, *args, **kwargs):
        return render(request, "user/manage.html")

class login_view(View):
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse("main"))
        return render(request, "user/login.html")

    def post(sefl, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse("main"))

@login_required(login_url = "login")
def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("login"))

def index(request):
    return render(request, "index.html")


main_urls = [
    url(r"^$", main_view.as_view(), name="main"),
    # url(r"^main/", main_view.as_view(), name="main"),
]

houses_urls = [
    url(r"^$", house_view.as_view(), name="house"),
    url(r"^add/", house_add_view.as_view(), name="house/add"),
]

manage_urls = [
    url(r"^$", manage_view.as_view(), name="manage"),
]

auth_urls = [
    url(r"^login/", login_view.as_view(), name="login"),
    url(r"^logout/", logout_view, name="logout"),
]

help_urls = [

]

urls = [
    url(r"^main/", include(main_urls)),
    url(r"^house/", include(houses_urls)),
    url(r"^manage/", include(manage_urls)),
    url(r"^help/", include(help_urls)),
    url(r"^auth/", include(auth_urls)),
]
