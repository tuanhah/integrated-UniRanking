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

    def __init__(self, *args, **kwargs):
        self.VIEWS_BY_METHOD = {
            'GET' : self.get_sectors,
        } 

    def get_sectors(self, request):
        sectors = Sector.objects.all()
        parsed_sector_list = [sector.parse_profile() for sector in sectors]
        return JsonResponse({"sectors" : parsed_sector_list})


