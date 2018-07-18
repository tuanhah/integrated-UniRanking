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
    path('', university_base_views.UniversityDetailView.as_view()),
    path('scores', university_score_views.UniversityScoreDetailView.as_view()),
]


criterion_url_paterns = [
    path('criteria', criterion_base_views.CriteriaOfCategoryListView.as_view()),
]

rank_url_patterns = [
    path("university", university_score_views.UniversityRankingView.as_view()),
    path("sector", subject_score_views.SubjectRankingView.as_view()),
]

urlpatterns = [
    path('auth',views.login, name="login"),
    path('register',views.register, name="register"),
    path('sectors', subject_base_views.SectorListView.as_view()),
    path('universities', university_base_views.UniversityListView.as_view()),
    path('universities/<int:university_id>/', include(university_url_patterns)),
    path('categories', criterion_base_views.CriterionCategoryListView.as_view()),
    path('categories/<int:category_id>/', include(criterion_url_paterns)),
    path('criteria', criterion_base_views.CriterionListView.as_view()),
    path("rank/", include(rank_url_patterns)),
]
