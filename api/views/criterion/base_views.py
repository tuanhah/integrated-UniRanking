from django.http import JsonResponse

from criterion.models import CriterionCategory
from api.functions import string_to_boolean
from api.views.base import BaseManageView

class CriterionCategoryListView(BaseManageView):
    """
        List all objects of criterion categories
        Model CriterionCategory
    """

    def __init__(self, *args, **kwargs):
        self.VIEWS_BY_METHOD = {
            'GET' : self.get_criterion_categories,
        } 

    def get_criterion_categories(self, request):
        request_data = request.GET
        target = request_data.get("target")
        if target == "subject":
            criterion_categories = CriterionCategory.objects.subject_only()
        elif target == 'university':
            criterion_categories = CriterionCategory.objects.university_only()
        else:
            criterion_categories = CriterionCategory.objects.all()
        parsed_categories = [category.parse_info() for category in criterion_categories]
        return JsonResponse(parsed_categories, safe = False)

class CriteriaOfCategoryListView(BaseManageView):
    """
        List all criteria of specific criterion category
        Model Criterion
    """

    error_messages = {
        "category" : {
            "invalid" : "This criterion category is invalid",
        },
    }

    def __init__(self, *args, **kwargs):
        self.VIEWS_BY_METHOD = {
            'GET' : self.get_criteria_of_category,
        }
    
    def get_criteria_of_category(self, request, category_id):
        try:
            criterion_category = CriterionCategory.objects.get(id = category_id)
        except CriterionCategory.DoesNotExist:
            return self.json_error(field = 'category', code = "invalid")
        result = criterion_category.parse_all_criterion_infos(named = True)
        return JsonResponse(result, safe = False)
        

class CriterionListView(BaseManageView):
    """
        List all criteria
        Model Criterion
    """

    def __init__(self, *args, **kwargs):
        self.VIEWS_BY_METHOD = {
            'GET' : self.get_sorted_criteria,
        }
    
    def get_sorted_criteria(self, request):
        request_data = request.GET
        target = request_data.get("target")
        if target == "university":
            criterion_categories = CriterionCategory.objects.university_only().prefetch_related("criteria")
        elif target == "subject":
            criterion_categories = CriterionCategory.objects.subject_only().prefetch_related("criteria")
        else:
            criterion_categories = CriterionCategory.objects.prefetch_related("criteria")
        result = []
        for criterion_category in criterion_categories:
            parsed_criterion_category = criterion_category.parse_info()
            parsed_criteria = criterion_category.parse_all_criterion_infos()
            result.append({"criterion_category" : parsed_criterion_category, "criteria" : parsed_criteria})
        return JsonResponse(result, safe = False)
        

