from django.contrib import admin

from .models import SubjectGroup, Subject, UniversitySubject, SubjectScoreByCriterionCategory, SubjectScoreByCriterion
from .forms import SubjectGroupForm, SubjectForm, UniversitySubjectForm, SubjectScoreByCriterionForm


@admin.register(SubjectGroup)
class SubjectGroupAdmin(admin.ModelAdmin):
    form = SubjectGroupForm

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    form = SubjectForm

@admin.register(UniversitySubject)
class UniversitySubjectAdmin(admin.ModelAdmin):
    form = UniversitySubjectForm

@admin.register(SubjectScoreByCriterionCategory)
class SubjectScoreByCriterionCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','university','subject','criterion_category','score')
    readonly_fields = ('univ_subject', 'criterion_category', 'score')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        pass

@admin.register(SubjectScoreByCriterion)
class UniversityScoreByCriterionAdmin(admin.ModelAdmin):
    form = SubjectScoreByCriterionForm
    list_display = ('id','university','subject','criterion','score')
    non_editable_fields = ('univ_subject', 'criterion')

    def get_readonly_fields(self, request, obj=None): 
        if obj is not None: 
            readonly_fields = self.readonly_fields + self.non_editable_fields
            return readonly_fields
        else:
            return self.readonly_fields