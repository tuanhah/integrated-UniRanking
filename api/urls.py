from django.urls import include, path
from . import views, criterion_views, subject_views, university_views

app_name = "api"


university_url_patterns = [
    path('scores', university_views.UniversityScoreDetailView.as_view()),
    path('subjects', university_views.UniversitySubjectListView.as_view()),
    path('subjects/<int:subject_id>', university_views.UniversitySubjectDetailView.as_view()),
    path('subjects/<int:subject_id>/scores', subject_views.SubjectScoreDetailView.as_view()),

]

subject_url_patterns = [
    path('groups', subject_views.GroupListView.as_view()),
    path('subjects', subject_views.SubjectsOfSectorListView.as_view()),
    path('groups/<int:group_id>/subjects', subject_views.SubjectListView.as_view()),
]

criterion_url_paterns = [
    path('criteria', criterion_views.CriteriaOfCategoryListView.as_view()),
]

rank_url_patterns = [
    path("subject/<int:subject_id>", subject_views.SubjectScoreListView.as_view()),
    path("university", university_views.UniversityScoreListView.as_view()),

]

urlpatterns = [
    path('auth',views.login, name="login"),
    path('register',views.register, name="register"),
    path('sectors', subject_views.SectorListView.as_view()),
    path('sectors/<int:sector_id>/', include(subject_url_patterns)),
    path('universities', university_views.UniversityListView.as_view()),
    path('universities/<int:university_id>/', include(university_url_patterns)),
    path('categories', criterion_views.CriterionCategoryListView.as_view()),
    path('categories/<int:category_id>/', include(criterion_url_paterns)),
    path('criteria/', criterion_views.CriterionListView.as_view()),
    path("rank/", include(rank_url_patterns)),
]
