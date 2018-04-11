from django.http import JsonResponse
from django.db.models import Prefetch, F
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from guardian.decorators import permission_required_or_403

from subject.models import SubjectGroup, SubjectScoreByCategory, SubjectScore 
from subject.forms import SubjectScoreForm, SubjectScoreAddForm, SubjectScoreEditForm, SubjectScoreDeleteForm
from university.models import University, UniversitySubject
from .base import BaseManageView, ScoreListView, ScoreDetailView
from .functions import json_error, string_to_boolean, get_all_scores_from_category_score, get_scores_of_object, get_category_scores_of_object

class GroupListView(BaseManageView):
    """
        List all subject sectors 
        Model SubjectGroup
    """

    error_messages = {
        "sector" : [
            {"code" : "invalid", "message" : "This sector is invalid"},
        ]
    }

    def __init__(self, *args, **kwargs):
        self.VIEWS_BY_METHOD = {
            'GET' : self.get_groups,
        } 

    def get_groups(self, request, sector_id):
        field = "sector"
        try:
            sector = SubjectGroup.objects.get(id = sector_id)
        except SubjectGroup.DoesNotExist:
            return json_error(field, self.error_messages)
        else:
            if sector.parent_id is not None: 
                return json_error(field, self.error_messages)
            else:
                groups = sector.groups.all()
                list_group = [{"id" : group.id, "name" : group.name} for group in groups]
                return JsonResponse(list_group, safe=False)


class SubjectsOfSectorListView(BaseManageView):
    """
        List all objects of particular sector based on UniversitySubject model
    """

    error_messages = {
        "sector" : [
            {"code" : "invalid", "message" : "This sector is invalid"},
        ]
    }

    def __init__(self, *args, **kwargs):
        self.VIEWS_BY_METHOD = {
            'GET' : self.get_subjects_of_sector,
        }

    def get_subjects_of_sector(self, request, sector_id):
        field = "sector"
        try:
            sector = SubjectGroup.objects.get(id = sector_id)
        except SubjectGroup.DoesNotExist:
            return json_error(field, self.error_messages)
        else:
            if sector.parent_id is not None: 
                return json_error(field, self.error_messages)
            else:
                groups_queryset = sector.groups.all().prefetch_related("subjects")
                result = []
                for group in groups_queryset:
                    group_id = group.id
                    group_name = group.name
                    subject_list = []   
                    for subject in group.subjects.all():
                        subject_list.append({"id" : subject.id, "name" : subject.name})
                    result.append({"id" : group_id, "name" : group_name, "subjects" : subject_list})
                return JsonResponse({"groups" : result}, safe=False) 

class SubjectListView(BaseManageView):
    """
        List all objects of particular sector based on UniversitySubject model
    """

    error_messages = {
        "group" : [
            {"code" : "invalid", "message" : "This group is invalid"},
        ]
    }

    def __init__(self, *args, **kwargs):
        self.VIEWS_BY_METHOD = {
            'GET' : self.get_subjects,
        }

    def get_subjects(self, request, sector_id, group_id):
        field = "group"
        try:
            group = SubjectGroup.objects.get(id = group_id)
        except SubjectGroup.DoesNotExist:
            return json_error(field, self.error_messages)
        else:
            if not group.parent_id == sector_id: 
                return json_error(field, self.error_messages)
            else:
                result = [] 
                subject_list = []
                for subject in group.subjects.all():
                    subject_list.append({"id" : subject.id, "name" : subject.name})
                result.append(subject_list)
                return JsonResponse(result, safe=False) 

class SubjectScoreListView(ScoreListView):
    """
        GET all scores of particular Subject sorted by University
    """

    def get_scores(self, request, subject_id):
        univ_subjects = UniversitySubject.objects.filter(
            subject_id = subject_id,
            rank__gt = 0
            ).select_related(
                "university"
            ).prefetch_related(
                Prefetch(
                    "scores_by_category",
                    queryset = SubjectScoreByCategory.objects.order_by(
                            "criterion_category_id"
                        ).select_related(
                            'criterion_category'
                        ).prefetch_related(
                            Prefetch('cri_scores', queryset=SubjectScore.objects.select_related('criterion'))
                        )   
                )
            )
        result = []
        for univ_subject in univ_subjects:
            university_id = univ_subject.university_id
            university_name = univ_subject.university.name
            university_href = univ_subject.university.get_absolute_url()
            scores_by_category = univ_subject.scores_by_category.all()
            scores = []
            for score_by_category in scores_by_category:
                data = get_all_scores_from_category_score(score_by_categorym, False)
                scores.append(data)
            result.append({"university" : {"id" : university_id, "university" : university_name, "href" : university_href}, "scores" : scores})
        return JsonResponse(result, safe=False)


class SubjectScoreDetailView(ScoreDetailView):
    """
        Manage to change/delete based on each subject's score of university
        Model SubjectScore (UniversitySubjectScore)
    """

    error_messages = {
        "category" : [
            {"code" : "invalid", "message" : "This category is invalid"},
        ],
        "__all__" : [
            {"code" : "invalid", "message" : "This university or subject is invalid"}
        ]
    }

    def get_scores(self, request, university_id, subject_id):
        try: 
            univ_subject = UniversitySubject.objects.annotate(
                subject_name = F('subject__name'),
            ).get(
                university = university_id,
                subject = subject_id
            )
        except UniversitySubject.DoesNotExist:
            field = "__all__"
            return json_error(field, self.error_messages)
        else:
            filter = request.GET.get("filter")
            labeled = string_to_boolean(request.GET.get("label"))
            result = {} 
            if filter == self.ScoresFiltering.ONLY_CATEGORY_SCORES:
                result["categoryScores"] = get_category_scores_of_object(univ_subject, labeled)
            elif filter == self.ScoresFiltering.ONLY_CRITERION_SCORES:
                #not implemented yet
                result = {"scores" : []}
            else:
                #filter == self.ScoresFiltering.ALL_SCORES
                result["score"] = get_scores_of_object(univ_subject, labeled)
            result["subject"] = univ_subject.subject_name
        return JsonResponse(result)
    
    @method_decorator(permission_required_or_403("university.change_university", (University, 'id', 'university_id')))
    def add_score(self, request, university_id, subject_id):
        try: 
            univ_subject = UniversitySubject.objects.get(university = university_id, subject = subject_id)
        except UniversitySubject.DoesNotExist:
            field = "__all__"
            return json_error(field, self.error_messages)
        else:
            request_data = request.POST
            input = {"univ_subject" : univ_subject.pk, "criterion" : request_data.get("criterion"), "score" : request_data.get("score")}
            score_form = SubjectScoreAddForm(input)
            if score_form.is_valid():
                score_form.save()
                return JsonResponse({"success" : "True"}, status = 201)
            else:
                error = score_form.errors.get_json_data()   
                return JsonResponse(error, status = 404)


    @method_decorator(permission_required_or_403("university.change_university", (University, 'id', 'university_id')))
    def edit_score(self, request, university_id, subject_id):
        try: 
            univ_subject = UniversitySubject.objects.get(university = university_id, subject = subject_id)
        except UniversitySubject.DoesNotExist:
            field = "__all__"
            return json_error(field, self.error_messages)
        else:
            request_data = request.PUT
            input = {"univ_subject" : univ_subject.pk, "criterion" : request_data.get("criterion"), "score" : request_data.get("score")}
            score_form = SubjectScoreEditForm(input)
            if score_form.is_valid():
                score_form.save()
                return JsonResponse({"success" : "True"})
            else:
                error = score_form.errors.get_json_data()   
                return JsonResponse(error, status = 404)

    @method_decorator(permission_required_or_403("university.change_university", (University, 'id', 'university_id')))
    def delete_score(self, request, university_id, subject_id):
        try: 
            univ_subject = UniversitySubject.objects.get(university = university_id, subject = subject_id)
        except UniversitySubject.DoesNotExist:
            field = "__all__"
            return json_error(field, self.error_messages)
        else:
            request_data = request.POST
            input = {"univ_subject" : univ_subject.pk, "criterion" : request_data.get("criterion"), "score" : 0}
            delete_form = SubjectScoreDeleteForm(input)
            if delete_form.is_valid():
                delete_form.delete_object()
                return JsonResponse({"success" : True}, status = 200)
            error = delete_form.errors.get_json_data()   
            return JsonResponse(error)
class SectorListView(BaseManageView):
    """
        List all subject sectors
        Model SubjectGroup
    """
    def __init__(self, *args, **kwargs):
        self.VIEWS_BY_METHOD = {
            'GET' : self.get_all_sectors,
        }
    def get_all_sectors(self, request):
        sectors = SubjectGroup.objects.filter(parent = None)
        list_sectors = [{"id": sector.id, "name" : sector.name} for sector in sectors]
        result = { "sectors" : list_sectors}
        return JsonResponse(result, safe = False)
    