from django.http import JsonResponse
from django.utils.decorators import method_decorator
from guardian.decorators import permission_required_or_403

from university.models import University
from subject.models import UniversitySector, Sector
# from subject.forms import SubjectScoreByCriterionCreateForm, SubjectScoreByCriterionEditForm
from api.views.base import BaseManageView, RankingView, ScoreDetailView
from api.functions import string_to_boolean
# from api.views.university.base_views import UniversityListView

class SubjectRankingView(RankingView):
    """
        GET University ranking of particular Subject
    """

    def get_ranking(self, request):
        request_data = request.GET
        search_keyword = request_data.get("search")
        sector_id = request_data.get("sector")
        if sector_id is None:
            universities_queryset = University.objects.prefetch_scores()
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
        universities = sorted(universities, key = lambda university: university.rank)
        result = {"universities" : [university.parse_data() for university in universities]}
        return JsonResponse(result) 

        