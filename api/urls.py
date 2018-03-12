from django.urls import include, path
from . import views

app_name = "api"

urlpatterns = [
    path('auth',views.login, name="login"),
    path('register',views.register, name="register"),
    path('scores',views.get_scores, name="get_scores"),
    path('subjects',views.get_subjects, name = 'get_subjects'),
    path('groups', views.get_groups_of_sector, name = "get_groups"),    
    path('editor/subjects/delete', views.delete_subject, name = "editor_delete_subject"),
    path('editor/subjects/add', views.add_subject, name="editor_add_subject"),
    path('editor/subjects', views.get_subjects_of_group, name="editor_get_subjects"),
    path('editor/scores/edit', views.edit_score, name="editor_edit_score"),
    path('editor/scores/delete', views.delete_score, name="editor_delete_score"),
    path('editor/criteria/categories', views.get_editable_criterion_categories, name="editor_get_editable_criterion_categories"),
    path('editor/criteria', views.get_criteria_of_category, name="editor_get_non_added_criteria_of_category"),
]