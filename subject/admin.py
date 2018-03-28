from django.contrib import admin

from .models import SubjectGroup, Subject, SubjectScore, SubjectScoreByCategory
from criteria.models import Criterion
from criteria.admin import ScoreAdmin
from .forms import SubjectScoreAddForm

admin.site.register(SubjectGroup)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id','name','group')

@admin.register(SubjectScoreByCategory)
class SubjectScoreByCategoryAdmin(ScoreAdmin):
    list_display = ('id','_university','_subject','criterion_category','score')
    readonly_fields = ('criterion_category','score','univ_subject')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        pass

@admin.register(SubjectScore)
class SubjectScoreAdmin(ScoreAdmin):
    form = SubjectScoreAddForm
    list_display = ('id','_university','_subject','criterion','score')
    