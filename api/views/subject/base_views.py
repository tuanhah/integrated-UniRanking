from django.http import JsonResponse
from django.db.models import Prefetch, F, Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from guardian.decorators import permission_required_or_403

from subject.models import Sector 
from university.models import University
from api.views.base import BaseManageView
from api.functions import string_to_boolean

class SectorListView(BaseManageView):
    """
        List all sectors 
        Model SubjectGroup
    """
    error_messages = {
        "university": {
            "invalid": "This university is invalid",
        },
        "sector": {
            "invalid": "This sector is invalid",
        }
    }


    def __init__(self, *args, **kwargs):
        self.VIEWS_BY_METHOD = {
            'GET' : self.get_sectors,
        } 

    def get_sectors(self, request):
        request_data = request.GET
        university_id = request_data.get('university')
        if university_id is None:
            sectors_queryset = Sector.objects.all()
        else:
            if not university_id.isdigit():
                return self.json_error(field='university', code='invalid')
            else:
                try:
                    university = University.objects.get(id = university_id)
                except University.DoesNotExist:
                    return self.json_error(field='university', code='invalid')
                else:
                    sectors_queryset = university.sector_set.all()

        parsed_sector_list = [sector.parse_profile() for sector in sectors_queryset]
        return JsonResponse({"sectors" : parsed_sector_list})

class UnasignSectorListView(BaseManageView):
    """
        List all sectors
        Model SubjectGroup
    """
    error_messages = {
        "university": {
            "invalid": "This university is invalid",
        },
        "sector": {
            "invalid": "This sector is invalid",
        }
    }


    def __init__(self, *args, **kwargs):
        self.VIEWS_BY_METHOD = {
            'GET' : self.get_unasign_sectors,
        }

    def get_unasign_sectors(self, request):
        request_data = request.GET
        university_id = request_data.get('university')
        if university_id is None:
            sectors_queryset = Sector.objects.all()
        else:
            if not university_id.isdigit():
                return self.json_error(field='university', code='invalid')
            else:
                try:
                    university = University.objects.get(id = university_id)
                except University.DoesNotExist:
                    return self.json_error(field='university', code='invalid')
                else:
                    sectors_queryset = university.sector_set.all()
        all_sectors = Sector.objects.all()

        unasign_sectors = list(set(all_sectors) - set(sectors_queryset))

        unasign_sector_list = [sector.parse_profile() for sector in unasign_sectors]
        return JsonResponse({"sectors" : unasign_sector_list})

