from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from .models import University, UniversityScore, UniversitySubject, UniversityScoreByCategory
from criteria.models import Criterion
from criteria.admin import ScoreAdmin
from .forms import UniversitySubjectForm, UniversityScoreForm

@admin.register(University)
class UniversityAdmin(GuardedModelAdmin):
    pass

@admin.register(UniversitySubject)
class UniversitySubjectAdmin(ScoreAdmin):
    list_display = ('id', 'university', 'subject')
    form = UniversitySubjectForm

@admin.register(UniversityScoreByCategory)
class UniversityScoreByCategoryAdmin(ScoreAdmin):
    list_display = ('id','university','criterion_category','score')
    readonly_fields = list_display

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        pass


@admin.register(UniversityScore)
class UniversityScoreAdmin(ScoreAdmin):
    form = UniversityScoreForm
    list_display = ('id','_university','criterion', 'score')