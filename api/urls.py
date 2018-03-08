from django.urls import include, path
from . import views

app_name = "api"

urlpatterns = [
    path('auth',views.login, name="login"),
    path('register',views.register, name="register"),
    path('score',views.get_scores, name="get_scores"),
]

