from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from django.contrib.admin import helpers
from django.utils.safestring import mark_safe

from .models import University, UniversityProfile, UniversityScoreByCriterion, UniversityScoreByCriterionCategory
from .forms import UniversityForm, UniversityProfileForm, UniversityScoreByCriterionForm
from score.admin import ScoreByCriterionCategoryAdmin

@admin.register(University)
class UniversityAdmin(GuardedModelAdmin):
    form = UniversityForm
    list_display = ('id', 'code', 'name', 'avg_score' ,'rank')
    readonly_fields = ('avg_score', 'rank')

@admin.register(UniversityProfile)
class UniversityProfile(admin.ModelAdmin):
    form = UniversityProfileForm


@admin.register(UniversityScoreByCriterionCategory)
class UniversityScoreByCriterionCategoryAdmin(ScoreByCriterionCategoryAdmin):
    list_display = ('id','university','criterion_category','score')
    readonly_fields = ('university','criterion_category','score')


@admin.register(UniversityScoreByCriterion)
class UniversityScoreByCriterionAdmin(admin.ModelAdmin):
    form = UniversityScoreByCriterionForm   
    list_display = ('id','university','criterion','score')
    non_editable_fields = ('university', 'criterion')
    
    def action_checkbox(self, obj):
        if obj is not None and not obj.is_editable:
            helpers.checkbox.attrs.update({"disabled" : True})
        else:
            helpers.checkbox.attrs.pop("disabled", None)
        return helpers.checkbox.render(helpers.ACTION_CHECKBOX_NAME, str(obj.pk))
    
    action_checkbox.short_description = mark_safe('<input type="checkbox" id="action-toggle">')

    def has_non_editable_object_in_delete_selected_object(self, request):
        request_data = request.POST
        if 'delete_selected' in request_data.get("action", []):
            selected_object_id = request_data.getlist("_selected_action")
            return UniversityScoreByCriterion.objects.filter(id__in = selected_object_id, criterion__category__university_only = False).exists()

    def has_delete_permission(self, request, obj=None):
        if (obj is not None and not obj.is_editable) or self.has_non_editable_object_in_delete_selected_object(request):
            return False  
        return super().has_delete_permission(request, obj)  

    def get_readonly_fields(self, request, obj=None): 
        if obj is not None: 
            readonly_fields = self.readonly_fields + self.non_editable_fields
            if not obj.is_editable:
                readonly_fields += ('score',)
            return readonly_fields
        else:
            return self.readonly_fields
