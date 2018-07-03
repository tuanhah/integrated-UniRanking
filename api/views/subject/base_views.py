from django.http import JsonResponse
from django.db.models import Prefetch, F, Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from guardian.decorators import permission_required_or_403

from subject.models import SubjectGroup, UniversitySubject 
from subject.forms import UniversitySubjectCreateForm, UniversitySubjectDeleteForm
from university.models import University
from api.views.base import BaseManageView
from api.functions import string_to_boolean

class SectorListView(BaseManageView):
    """
        List all sectors 
        Model SubjectGroup
    """

    def __init__(self, *args, **kwargs):
        self.VIEWS_BY_METHOD = {
            'GET' : self.get_sectors,
        } 

    def get_sectors(self, request):
        sectors = SubjectGroup.objects.filter(sector_id = None)
        parsed_sector_list = [sector.parse_profile() for sector in sectors]
        return JsonResponse({"sectors" : parsed_sector_list})


class GroupListView(BaseManageView):
    """
        List all group 
        Model SubjectGroup
    """

    error_messages = {
        "sector" : {
            "invalid" : "This sector is invalid",
        }
    }

    def __init__(self, *args, **kwargs):
        self.VIEWS_BY_METHOD = {
            'GET' : self.get_groups,
        } 

    def get_groups(self, request, sector_id):
        try:
            sector = SubjectGroup.objects.get(id = sector_id, sector_id = None)
        except SubjectGroup.DoesNotExist:
            return self.json_error(field = 'sector', code = "invalid")
        else:
            groups = sector.groups.all()
            parsed_group_list = [group.parse_profile() for group in groups] 
            return JsonResponse({"groups" : parsed_group_list})


class SubjectsOfSectorListView(BaseManageView):
    """
        List all subjects of specific sector
        Model Subject
    """

    error_messages = {
        "sector" : {
            "invalid" : "This sector is invalid",
        }
    }

    def __init__(self, *args, **kwargs):
        self.VIEWS_BY_METHOD = {
            'GET' : self.get_subjects_of_sector,
        }

    def get_subjects_of_sector(self, request, sector_id):
        try:
            sector = SubjectGroup.objects.get(id = sector_id, sector_id = None)
        except SubjectGroup.DoesNotExist:
            return self.json_error(field = 'sector', code = "invalid")
        else:
            group_queryset = sector.groups.all().prefetch_related("subjects")
            sorted_subjects = [] 
            for group in group_queryset:
                parsed_group = group.parse_profile()
                parsed_subject_list = group.parse_all_subject_profiles()
                sorted_subjects.append({"group" : parsed_group, "subjects" : parsed_subject_list})
            result = {"sorted_subjects" : sorted_subjects}
            return JsonResponse(result) 

class SubjectOfGroupListView(BaseManageView):
    """
        List all subjects of specific group
        Model Subject
    """

    error_messages = {
        "group" : {
            "invalid" : "Sector or group is invalid",
        }
    }

    def __init__(self, *args, **kwargs):
        self.VIEWS_BY_METHOD = {
            'GET' : self.get_subjects,
        }

    def get_subjects(self, request, sector_id, group_id):
        try:
            group = SubjectGroup.objects.get(id = group_id, sector_id = sector_id)
        except SubjectGroup.DoesNotExist:
            return self.json_error(field = 'group', code = 'invalid')
        else:
            parsed_subject_list = group.parse_all_subject_profiles()
            return JsonResponse({"subjects" : parsed_subject_list}) 

class UniversitySubjectListView(BaseManageView):
    """
        List all subjects of specific university
        Model UniversitySubject
    """

    error_messages = {
        "group" : {
            "invalid" : "This group is invalid",
        },
        "university" : {
            "invalid" : "This university is invalid",
        },
    }

    def __init__(self, *args, **kwargs):
        self.VIEWS_BY_METHOD = {
            'GET' : self.get_subjects,
        } 

    def get_subjects(self, request, university_id):
        try:
            university = University.objects.get(id = university_id)
        except University.DoesNotExist:
            return self.json_error(field = 'university', code = "invalid")
        else:
            group_id = request.GET.get('group')
            if group_id is not None:
                if not group_id.isdigit():
                    return self.json_error(field = 'group', code = "invalid")
                try:
                    group = SubjectGroup.objects.get(Q(id = group_id) & ~Q(sector_id = None))
                except SubjectGroup.DoesNotExist:
                    return self.json_error(field = 'group', code = "invalid")
                else:
                    subject_list = university.parse_university_subjects_of_group(group)
                    return JsonResponse({"subjects" : subject_list})
            else:
                sorted_subjects = university.parse_sorted_university_subjects()
                return JsonResponse({"sorted_subjects" : sorted_subjects})  


class UniversitySubjectDetailView(BaseManageView):
    """
        Manage to change/delete based on UniversitySubject model
    """

    error_messages = {
        "__all__" : {
            "invalid" : "This university or subject is invalid",
        }
    }
    
    def __init__(self, *args, **kwargs):
        self.VIEWS_BY_METHOD = {
            'GET' : self.get_subject,
            'POST' : self.add_subject,
            'DELETE' : self.delete_subject, 
        }  
    
    def get_subject(self, request, university_id, subject_id):
        try: 
            univ_subject = UniversitySubject.objects.select_related(
                "university",
                "subject"
            ).get(
                university = university_id,
                subject = subject_id
            )
        except UniversitySubject.DoesNotExist:
            return self.json_error(field = '__all__', code = "invalid")
        else:
            result = univ_subject.parse_profile()
            return JsonResponse(result)


    @method_decorator(permission_required_or_403("university.change_university", (University, 'id', 'university_id')))
    def add_subject(self, request, university_id, subject_id):
        form = UniversitySubjectCreateForm({"university" : university_id, "subject" : subject_id})
        if form.is_valid():
            form.save()
            return JsonResponse({"success" : True}, status = 201)
        else:
            error = form.errors.get_json_data()   
            return JsonResponse(error, status = 404)

    @method_decorator(permission_required_or_403("university.change_university", (University, 'id', 'university_id')))
    def delete_subject(self, request, university_id, subject_id):
        delete_form = UniversitySubjectDeleteForm({"university" : university_id, "subject" : subject_id})
        if delete_form.is_valid():
            delete_form.delete()
            return JsonResponse({"success" : True}, status = 200)
        else:
            error = delete_form.errors.get_json_data()  
            return JsonResponse(error, status = 404)

