from django.urls import include, path
from .views import views
from .views.university import (
    base_views as university_base_views,
    score_views as university_score_views
)
from .views.subject import (
    base_views as subject_base_views,
    score_views as subject_score_views,
)
from .views.criterion import (
    base_views as criterion_base_views,
)
app_name = "api"


university_url_patterns = [
    path('subjects', subject_base_views.UniversitySubjectListView.as_view()),
    path('subjects/<int:subject_id>', subject_base_views.UniversitySubjectDetailView.as_view()),
    path('scores', university_score_views.UniversityScoreDetailView.as_view()),
    path('subjects/<int:subject_id>/scores', subject_score_views.SubjectScoreDetailView.as_view()),
]

subject_url_patterns = [
    path('groups', subject_base_views.GroupListView.as_view()),
    path('subjects', subject_base_views.SubjectsOfSectorListView.as_view()),
    path('groups/<int:group_id>/subjects', subject_base_views.SubjectOfGroupListView.as_view()),
]

criterion_url_paterns = [
    path('criteria', criterion_base_views.CriteriaOfCategoryListView.as_view()),
]

rank_url_patterns = [
    path("university", university_score_views.UniversityRankingView.as_view()),
    path("subject/<int:subject_id>", subject_score_views.SubjectRankingView.as_view()),
]

urlpatterns = [
    path('auth',views.login, name="login"),
    path('register',views.register, name="register"),
    path('sectors', subject_base_views.SectorListView.as_view()),
    path('sectors/<int:sector_id>/', include(subject_url_patterns)),
    path('universities', university_base_views.UniversityListView.as_view()),
    path('universities/<int:university_id>/', include(university_url_patterns)),
    path('categories', criterion_base_views.CriterionCategoryListView.as_view()),
    path('categories/<int:category_id>/', include(criterion_url_paterns)),
    path('criteria', criterion_base_views.CriterionListView.as_view()),
    path("rank/", include(rank_url_patterns)),
]
