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
        List all universities 
        University model
    """

    error_messages = {
        "subject" : {
            "invalid" : "This subject is invalid",
        },
    }

    def __init__(self, *args, **kwargs):
        self.VIEWS_BY_METHOD = {
            'GET' : self.get_universities,
        } 

    def get_universities(self, request):
        request_data = request.GET
        search_keyword = request_data.get("search")
        subject_id = request_data.get("subject")
        if subject_id is None:
            universities_queryset = University.objects.all()
        else:
            if not subject_id.isdigit():
                return self.json_error(field = 'subject', code = "invalid")
            else:
                try:
                    subject = Subject.objects.get(id = subject_id)
                except Subject.DoesNotExist:
                    return self.json_error(field = 'subject', code = "invalid")
                else:
                    universities_queryset = subject.university_set.all()
        if search_keyword is not None: 
            universities = universities_queryset.filter(name__icontains = search_keyword)            
        else: 
            universities = universities_queryset
        result = [university.parse_basic_info() for university in universities]
        return JsonResponse(result, safe=False)