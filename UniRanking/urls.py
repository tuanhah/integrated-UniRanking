"""UniRanking URL Configuration

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

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # path('', TemplateView.as_view(template_name ="index.html"), name = "homepage"),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace="api")),
    path('logout',LogoutView.as_view(), name = "logout"),
    path('register/',views.register,name="register"),
    path('university/', include('university.urls')),
    path('', views.index, name="index"),
    path('index/', views.index, name="index"),
    path('compare/', views.compare, name="compare"),
    path('university-info/', views.info, name="info"),
    path('contact/', views.contact, name="contact"),
    path('help/', views.help, name="help"),
    path('login/', views.login, name="login"),
    path('ranking/', views.ranking, name="ranking")
]
