from django.http import JsonResponse

from criteria.models import CriterionCategory
from .functions import json_error
from .base import BaseManageView

class CriterionCategoryListView(BaseManageView):
    """
        List all objects of criterion categories
        Model CriterionCategory
    """

    error_messages = {
        "target" : [
            {"code" : "invalid", "message" : "This target is invalid"},
        ],
    }

    def __init__(self, *args, **kwargs):
        self.VIEWS_BY_METHOD = {
            'GET' : self.get_criterion_categories,
        } 

    def get_criterion_categories(self, request):
        request_data = request.GET
        target = request_data.get("target")
        field = "target"
        if target == "subject":
            categories_queryset = CriterionCategory.objects.filter(university_only = False)
        elif target == 'university':
            all = request_data.get("all") or "true" #default is true
            if all == "true":
                categories_queryset = CriterionCategory.objects.all()
            else:
                categories_queryset = CriterionCategory.objects.filter(university_only = True)
        else:
            return json_error(field, self.error_messages)
        result = []
        for category in categories_queryset:
            category_id = category.id
            category_name = category.name
            criterion_list = []
            for criterion in category.criteria.all():
                criterion_list.append({"id" : criterion.id, "name" : criterion.name, "description" : criterion.description})
            result.append({"id" : category_id, "name" : category_name, "criteria" : criterion_list})
        return JsonResponse({"categories": result}, safe = False)

class CriteriaOfCategoryListView(BaseManageView):
    """
        List all objects of criteria 
        Model Criterion
    """

    error_messages = {
        "category" : [
            {"code" : "invalid", "message" : "This criterion category is invalid"},
        ],
    }

    def __init__(self, *args, **kwargs):
        self.VIEWS_BY_METHOD = {
            'GET' : self.get_criteria_of_category,
        }
    
    def get_criteria_of_category(self, request, category_id):
        try:
            criterion_category = CriterionCategory.objects.get(id = category_id)
        except CriterionCategory.DoesNotExist:
            field = "category"
            return json_error(field, self.error_messages)
        criterion_category_id = criterion_category.id
        criterion_category_name = criterion_category.name
        criteria = []
        for criterion in criterion_category.criteria.all():
            criteria.append({ "id" : criterion.id, "name" : criterion.name, "description" : criterion.description})
        result = ({"id" : criterion_category_id, "name" : criterion_category_name, "criteria" : criteria})
        return JsonResponse({"CategoryWithCriterions" : result}, safe = False)
        

class CriterionListView(BaseManageView):
    """
        List all objects of Criterion Model 
        Model Criterion
    """

    def __init__(self, *args, **kwargs):
        self.VIEWS_BY_METHOD = {
            'GET' : self.get_sorted_criteria,
        }
    
    def get_sorted_criteria(self, request):
        criterion_categories = CriterionCategory.objects.prefetch_related("criteria")
        result = []
        for criterion_category in criterion_categories:
            criterion_category_id = criterion_category.id
            criterion_category_name = criterion_category.name
            criteria = []
            for criterion in criterion_category.criteria.all():
                criteria.append({ "id" : criterion.id, "name" : criterion.name, "description" : criterion.description})
            result.append({"id" : criterion_category_id,"name" : criterion_category_name, "criteria" : criteria})
        return JsonResponse(result, safe = False)
        

