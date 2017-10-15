"""fluData URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include,url
from django.contrib import admin
from . import views
from . import Users
from django.views.generic import TemplateView

# mainUrls=[
#
# ]
#
# houseUrls=[
#
# ]
#
# clientUrls=[
#
# ]
#
# achievementUrls=[
#
# ]

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



urlpatterns = [
    url(r'^$',views.index),
    url(r'^admin/', admin.site.urls),
    url(r'^user/',include(Users.userUrls)),
    url(r'^test/',Users.userv.testv,name="test"),
]
