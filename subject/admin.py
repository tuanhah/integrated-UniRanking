from django.contrib import admin
from .models import GroupSubject, Subject, SubjectScore, SubjectScoreByCategory
from criteria.models import Criterion
from .forms import SubjectScoreForm

admin.site.register(GroupSubject)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id','name','group')

@admin.register(SubjectScoreByCategory)
class SubjectScoreByCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','_university','_subject','category_criterion','score')
    readonly_fields = ('category_criterion','score','univ_subject')

@admin.register(SubjectScore)
class SubjectScore(admin.ModelAdmin):
    form = SubjectScoreForm
    list_display = ('id','_university','_subject','criterion','score')