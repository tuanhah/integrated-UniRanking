"""UniRanking_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.urls import path
from django.conf import settings

from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('test/', views.test),
    # path('', TemplateView.as_view(template_name ="index.html"), name = "homepage"),
    path('university/', include('university.urls')),
    path('api/v1/', include("api.urls")),

    path('', views.index, name="index"),
    path('compare/', views.compare, name="compare"),
    path('university-info/', views.info, name="info"),
    path('ranking/', views.ranking, name="ranking"),
    path('contact/', views.contact, name="contact"),
    path('help/', views.help, name="help"),
    path('register/', views.register, name="register"),
    path('rank/', views.rank, name="rank"),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns