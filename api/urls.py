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
from .views.user import (
    favourite_views as user_favourite_views,
    manage_views as user_manage_views,
)
from .views.crud import (
    sector as edit_sector,
    university_score as edit_university_score,
    university_sector as edit_university_sector,
    favourite_university as edit_favourite_university
)
app_name = "api"

user_url_patterns = [
    path('favourite', user_favourite_views.FavouriteUniversityListView.as_view()),
    path('manage', user_manage_views.ManageUniversityListView.as_view())
]

edit_url_patterns = [
    path('sector/add_sector', edit_sector.add_sector, name="add_sector"),
    path('sector/update_sector', edit_sector.update_sector, name="update_sector"),
    path('sector/remove_sector', edit_sector.remove_sector, name="remove_sector"),
    path('favourite/add_university', edit_favourite_university.add_favourite_university, name="add_favourite"),
    path('favourite/remove_university', edit_favourite_university.remove_favourite_university, name="remove_favourite"),

]


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
    path('unasign-sectors', subject_base_views.UnasignSectorListView.as_view()),
    path('universities', university_base_views.UniversityListView.as_view()),
    path('universities/<int:university_id>/', include(university_url_patterns)),
    path('categories', criterion_base_views.CriterionCategoryListView.as_view()),
    path('categories/<int:category_id>/', include(criterion_url_paterns)),
    path('criteria', criterion_base_views.CriterionListView.as_view()),
    path("rank/", include(rank_url_patterns)),
    path('user/', include(user_url_patterns)),
    path('edit/', include(edit_url_patterns)),
]
