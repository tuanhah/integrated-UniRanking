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
from django.urls import path, include
from django.conf import settings

from . import views

user_urlpatterns = [
    path('overview/', views.overview, name="overview"),
    path('favourite-university', views.favourite_university, name="favourite-university"),
    path('manage-university', views.manage_university, name="manage-university"),
    path('manage-sector', views.manage_sector, name="manage-sector"),
    path('me', views.personal, name="personalpage"),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('university/', include('university.urls')),
    path('api/v1/', include("api.urls")),
    path('', views.index, name="homepage"),
    path('compare/', views.compare, name="compare"),
    path('search-info/', views.info, name="info"),
    path('rank/', views.rank, name="ranking"),
    path('contact/', views.contact, name="contact"),
    path('help/', views.help, name="help"),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('logout', auth.views.logout),
    path('user/', include(user_urlpatterns)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns