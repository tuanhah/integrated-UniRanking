from django.urls import include, path
from . import views

urlpatterns = [
    path('<int:id>/',views.university_info, name="university_profile"),
]

