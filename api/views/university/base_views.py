from django.http import JsonResponse
from django.db.models import Prefetch, Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from guardian.decorators import permission_required_or_403

from university.models import University
from subject.models import Sector, UniversitySector
from api.views.base import BaseManageView
from api.functions import string_to_boolean

class UniversityListView(BaseManageView):
    """ 
        List all universities (base on subject)
        University model
    """

    error_messages = {
        "subject" : {
            "invalid" : "This subject is invalid",
        },
        "sector" : {
            "invalid" : "This sector is invalid",
        }
    }

    def __init__(self, *args, **kwargs):
        self.VIEWS_BY_METHOD = {
            'GET' : self.get_universities,
        } 

    def get_universities(self, request):
        request_data = request.GET
        search_keyword = request_data.get("search")
        sector_id = request_data.get("sector")
        if sector_id is None:
            universities_queryset = University.objects.all()
        else:
            if not sector_id.isdigit():
                return self.json_error(field = 'subject', code = "invalid")
            else:
                try:
                    sector = Sector.objects.get(id = sector_id)
                except Sector.DoesNotExist:
                    return self.json_error(field = 'subject', code = "invalid")
                else:
                    universities_queryset = sector.university_set.all()

        if search_keyword is not None:
            universities = universities_queryset.filter(name__icontains = search_keyword)            
        else:
            universities = universities_queryset
        result = {"universities" : [university.parse_basic_info() for university in universities]}
        return JsonResponse(result) 

class UniversityDetailView(BaseManageView):
    """ 
        Get specific university profile
        University model
    """

    error_messages = {
        "university" : {
            "invalid" : "This university is invalid",
        },
    }

    def __init__(self, *args, **kwargs):
        self.VIEWS_BY_METHOD = {
            'GET' : self.get_university,
        } 

    def get_university(self, request, university_id):
        try:
            university = University.objects.get(pk = university_id)
        except University.DoesNotExist:
            return self.json_error(field = 'university', code = 'invalid')
        else:
            result = university.parse_full_profile()
            return JsonResponse(result)
    