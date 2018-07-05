from django.http import JsonResponse
from django.db.models import Prefetch, Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from guardian.decorators import permission_required_or_403

from university.models import University
from subject.models import SubjectGroup, Subject, UniversitySubject
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

    def get_universities_queryset(self, request):
        request_data = request.GET
        search_keyword = request_data.get("search")
        sector_id = request_data.get("sector")
        universities_queryset = []
                    
        if sector_id is None:
            universities_queryset = University.objects.all()
        else:
            if not sector_id.isdigit():
                return self.error_messages["sector"]["invalid"]
                # return self.json_error(field = 'sector', code = "invalid")
            else:
                try:
                    sector = SubjectGroup.objects.get(id = sector_id, sector_id = None)
                except SubjectGroup.DoesNotExist:
                    return self.error_messages["sector"]["invalid"]          
                    # return self.json_error(field = 'sector', code = "invalid")          
                else:
                    group_queryset = sector.groups.all().prefetch_related("subjects")
                    sorted_subjects = []
                    for group in group_queryset:
                        parsed_subject_list = group.parse_all_subject_profiles()
                        sorted_subjects.extend(parsed_subject_list)
                    # sector_universities = []
                    for sorted_subject in sorted_subjects:
                        subject_id = sorted_subject['id']
                        try:
                            subject = Subject.objects.get(id = subject_id)
                        except Subject.DoesNotExist:
                            return self.error_messages["subject"]["invalid"]
                            # return self.json_error(field = 'subject', code = "invalid")
                        else:
                            subject_universities = subject.university_set.all()
                            if search_keyword is not None: 
                                universities_per_subject = subject_universities.filter(name__icontains = search_keyword)            
                            else: 
                                universities_per_subject = subject_universities
                                for university in universities_per_subject:
                                    if university not in universities_queryset:
                                        universities_queryset.append(university)
                    return universities_queryset

    def get_universities(self, request):
        universities_queryset = self.get_universities_queryset(request)
        result = {}
        if type(universities_queryset) is list:
            result = {"universities" : [university.parse_basic_info() for university in universities_queryset]}
        elif universities_queryset == self.error_messages["sector"]["invalid"]:
            result["message"] =  self.error_messages["sector"]["invalid"]
        elif universities_queryset == self.error_messages["subject"]["invalid"]:
            result["message"] =  self.error_messages["subject"]["invalid"]
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
    