from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from .models import University, UniversityProfile, UniversityScoreByCriterion, UniversityScoreByCriterionCategory
from .forms import UniversityForm, UniversityProfileForm, UniversityScoreByCriterionForm

@admin.register(University)
class UniversityAdmin(GuardedModelAdmin):
    form = UniversityForm

@admin.register(UniversityProfile)
class UniversityProfile(admin.ModelAdmin):
    form = UniversityProfileForm


@admin.register(UniversityScoreByCriterionCategory)
class UniversityScoreByCriterionCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','university','criterion_category','score')
    readonly_fields = ('university','criterion_category','score')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        pass


@admin.register(UniversityScoreByCriterion)
class UniversityScoreByCriterionAdmin(admin.ModelAdmin):
    form = UniversityScoreByCriterionForm   
    list_display = ('id','university','criterion','score')
    non_editable_fields = ('university', 'criterion')

    def has_delete_permission(self, request, obj=None):
        if obj is not None and not obj.is_editable:
            return False  
        return super().has_delete_permission(request, obj)  

    def get_readonly_fields(self, request, obj=None): 
        if obj is not None: 
            readonly_fields = self.readonly_fields + self.non_editable_fields
            if not obj.is_editable:
                readonly_fields.extend(['score'])
            return readonly_fields
        else:
            return self.readonly_fields