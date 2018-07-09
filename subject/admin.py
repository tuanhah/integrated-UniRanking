from django.contrib import admin

from .models import Sector, UniversitySector
from .forms import SectorForm, UniversitySectorForm
# from score.admin import ScoreByCriterionCategoryAdmin


# @admin.register(SubjectGroup)
# class SubjectGroupAdmin(admin.ModelAdmin):
#     form = SubjectGroupForm
#     list_display = ('id', 'name', 'is_sector', 'is_group')

# @admin.register(Subject)
# class SubjectAdmin(admin.ModelAdmin):
#     form = SubjectForm
#     list_display = ('id', 'name', 'group')

# @admin.register(UniversitySubject)
# class UniversitySubjectAdmin(admin.ModelAdmin):
#     form = UniversitySubjectForm
#     list_display = ('id', 'university', 'subject', 'avg_score', 'rank')
#     readonly_fields = ('avg_score', 'rank')

# @admin.register(SubjectScoreByCriterionCategory)
# class SubjectScoreByCriterionCategoryAdmin(ScoreByCriterionCategoryAdmin):
#     list_display = ('id','university','subject','criterion_category','score')
#     readonly_fields = ('univ_subject', 'criterion_category', 'score')

#     def has_add_permission(self, request):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False

#     def save_model(self, request, obj, form, change):
#         pass

# @admin.register(SubjectScoreByCriterion)
# class UniversityScoreByCriterionAdmin(admin.ModelAdmin):
#     form = SubjectScoreByCriterionForm
#     list_display = ('id','university','subject','criterion','score')
#     non_editable_fields = ('univ_subject', 'criterion')

#     def get_readonly_fields(self, request, obj=None): 
#         if obj is not None: 
#             readonly_fields = self.readonly_fields + self.non_editable_fields
#             return readonly_fields
#         else:
#             return self.readonly_fields

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
	form = SectorForm
	list_display = ('id', 'name')

@admin.register(UniversitySector)
class UniversitySectorAdmin(admin.ModelAdmin):
	form = UniversitySectorForm
	list_display = ('id', 'university', 'sector')