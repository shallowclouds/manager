#coding=UTF-8


from django.http import HttpResponse
# from django.template import context
from django.shortcuts import render
from django.template import Template, Context
from django.template.loader import get_template
from django.http import HttpResponseRedirect
from django.urls import reverse


def index(request):
    # print(request.POST["userName"])
    # if request.method=="GET":
    # print(request.method)
    return render(request, "index.html")


class User_API():
    pass
