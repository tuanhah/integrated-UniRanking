from django.http import JsonResponse
from django.utils.decorators import method_decorator
from guardian.decorators import permission_required_or_403
from university.models import University
from university.forms import UniversityScoreByCriterionCreateForm, UniversityScoreByCriterionEditForm
from api.views.base import RankingView, ScoreDetailView
from api.functions import string_to_boolean

class UniversityRankingView(RankingView):
    """
        GET all scores sorted by University
    """

    def get_ranking(self, request):
        
        universities = University.objects.order_by_rank().prefetch_scores()
        result = {"rank" : [university.parse_data() for university in universities]}
        return JsonResponse(result)

class UniversityScoreDetailView(ScoreDetailView):
    """
         Manage to change/delete based on university's score 
         Model UniversityScoreByCriterion
    """

    error_messages = {
        "category" : {
            "invalid" : "This category is invalid",
        },
        "university" : {
            "invalid" : "This university is invalid",
        }
    
    }

    def get_scores(self, request, university_id):
        filter = request.GET.get("filter")
        named = string_to_boolean(request.GET.get("named"))
        result = {}
        if filter == self.ScoresFiltering.ONLY_CATEGORY_SCORES:
            try: 
                university = University.objects.prefetch_criterion_category_scores().get(id = university_id)
            except University.DoesNotExist:
                return self.json_error(field = 'university', code = "invalid")
            else:
                result["categoryScores"] = university.parse_criterion_category_scores(named = named)
        elif filter == self.ScoresFiltering.ONLY_CRITERION_SCORES:
            #not implemented yet
            result = {"scores" : []}
        else:
            #filter == self.ScoresFiltering.ALL_SCORES
            try: 
                university = University.objects.prefetch_scores().get(id = university_id)
            except University.DoesNotExist:
                return self.json_error(field = 'university', code = "invalid")
            else:
                result["scores"] = university.parse_scores(named = named)
                
        university_info = university.parse_basic_info()
        result["profile"] = {"university" : university_info}
        return JsonResponse(result)

    @method_decorator(permission_required_or_403("university.change_university", (University, 'id', 'university_id')))
    def add_score(self, request, university_id):
        request_data = request.POST
        input = {"university" : university_id, "criterion" : request_data.get("criterion"), "score" : request_data.get("score")}
        score_form = UniversityScoreByCriterionCreateForm(input)
        if score_form.is_valid():
            score_form.save()
            return JsonResponse({"success" : True}, status = 201)
        else:
            error = score_form.errors.get_json_data()   
            return JsonResponse(error)


    @method_decorator(permission_required_or_403("university.change_university", (University, 'id', 'university_id')))
    def edit_score(self, request, university_id):
        request_data = request.PUT
        input = {"university" : university_id, "criterion" : request_data.get("criterion"), "score" : request_data.get("score")}
        score_edit_form = UniversityScoreByCriterionEditForm(input)
        if score_edit_form.is_valid():
            score_edit_form.save()
            return JsonResponse({"success" : True})
        else:
            error = score_edit_form.errors.get_json_data()   
            return JsonResponse(error)

    @method_decorator(permission_required_or_403("university.change_university", (University, 'id', 'university_id')))
    def delete_score(self, request, university_id):
        request_data = request.DELETE
        input = {"university" : university_id, "criterion" : request_data.get("criterion"), "score" : 0}
        delete_form = UniversityScoreByCriterionEditForm(input)
        if delete_form.is_valid():
            delete_form.delete()
            return JsonResponse({"success" : True})
        else:
            error = delete_form.errors.get_json_data()   
            return JsonResponse(error)