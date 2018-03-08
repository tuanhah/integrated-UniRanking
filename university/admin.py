from django.contrib import admin
from .models import University, UniversityScore, UniversitySubject, UniversityScoreByCategory
from criteria.models import Criterion
from .forms import UniversityScoreForm

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    pass
    # list_display = ('id','code','name','ranking_position')

@admin.register(UniversityScoreByCategory)
class UniversityScoreByCategory(admin.ModelAdmin):
    list_display = ('id','university','category_criterion','score')
    readonly_fields = list_display

@admin.register(UniversityScore)
class UniversityScore(admin.ModelAdmin):
    form = UniversityScoreForm
    list_display = ('id','_university','criterion','score')

@admin.register(UniversitySubject)
class UniversitySubjectAdmin(admin.ModelAdmin):
    list_display = ('id','university','subject')