from django.http import JsonResponse
from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from guardian.decorators import permission_required_or_403

from university.models import University, UniversitySubject, UniversityScoreByCategory, UniversityScore
from university.forms import (UniversitySubjectDeleteForm, UniversitySubjectCreateForm, UniversityScoreForm, 
                                UniversityScoreAddForm, UniversityScoreEditForm, UniversityScoreDeleteForm)
from subject.models import SubjectGroup, Subject
from .base import BaseManageView, ScoreListView, ScoreDetailView
from .functions import (json_error, string_to_boolean, get_all_scores_from_category_score, get_sorted_univ_subjects, 
                            get_all_subjects_of_group,get_scores_of_object, get_category_scores_of_object)

class UniversityListView(BaseManageView):
    """
        List all universities
        University model
    """

    error_messages = {
        "subject" : [
            {"code" : "invalid", "message": "This subject is invalid"},
        ],

    }
  
    def __init__(self, *arg, **kwargs):
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
            field = "subject"
            if not subject_id.isdigit():
                return json_error(field, self.error_messages)
            else:
                try:    
                    subject = Subject.objects.get(id = subject_id)
                except Subject.DoesNotExist:
                    return json_error(field, self.error_messages)
                else:
                    universities_queryset = subject.university_set.all()
        if search_keyword is not None:
            universities = universities_queryset.filter(name__icontains = search_keyword)
        else:
            universities = universities_queryset 
        result = [{"id" : university.id, "name" : university.name} for university in universities]
        return JsonResponse(result, safe = False)

class UniversitySubjectListView(BaseManageView):
    """
        List all objects based on UniversitySubject model
    """
    
    eror_messages = {
        "group" : [
            {"code" : "invalid", "message" : "This group is invalid"},
        ],
        "university" : [
            {"code" : "invalid", "message" : "This university is invalid"}
        ],
    }

    def __init__(self, *args, **kwargs):
        self.VIEWS_BY_METHOD = {
            'GET' : self.get_subjects,
        } 

    def get_subjects(self, request, university_id):

        field = 'university'
        try:
            university = University.objects.get(id = university_id)
        except University.DoesNotExist:
            return json_error(field, self.error_messages)
        else:
            group_id = request.GET.get('group')
            if group_id is not None:
                field = 'group'
                if not group_id.isdigit():
                    return json_error(field, self.error_messages)
                try:
                    group = SubjectGroup.objects.get(id = group_id)
                except SubjectGroup.DoesNotExist:
                    return json_error(field, self.error_messages)
                else:
                    if group.parent_id is None: 
                        return json_error(field, self.error_messages)
                    else:
                        list_subject = get_all_subjects_of_group(university, group)
                        return JsonResponse(list_subject, safe=False)
            else:
                name = university.name
                sorted_subjects = get_sorted_univ_subjects(university)
                result = {"university" : name, "sorted_subjects" : sorted_subjects}
                return JsonResponse(result)  


class UniversitySubjectDetailView(BaseManageView):
    """
        Manage to change/delete based on UniversitySubject model
    """

    error_messages = {
        "__all__" : [
            {"code" : "invalid", "message" : "This university or subject is invalid"}
        ]
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
            field = "__all__"
            return json_error(field, self.error_messages)
        else:
            university = univ_subject.university
            subject = univ_subject.subject
            return JsonResponse({
                "university" : {"id" : university.id, "name" : university.name}, 
                "subject" : {"id" : subject.id, "name" : subject.name},
                "overall_score" : univ_subject.overall_score,
                "rank" : univ_subject.rank
            })
    
    @method_decorator(permission_required_or_403("university.change_university", (University, 'id', 'university_id')))
    def add_subject(self, request, university_id, subject_id):
        form = UniversitySubjectCreateForm({"university" : university_id, "subject" : subject_id})
        if form.is_valid():
            form.save()
            return JsonResponse({"success" : True}, status = 201)
        error = form.errors.get_json_data()   
        return JsonResponse(error, status = 404)

    @method_decorator(permission_required_or_403("university.change_university", (University, 'id', 'university_id')))
    def delete_subject(self, request, university_id, subject_id):
        form = UniversitySubjectDeleteForm({"university" : university_id, "subject" : subject_id})
        if form.is_valid():
            univ_subject = form.get_univ_subject_object()
            print(univ_subject.id)
            subject = univ_subject.subject.name
            univ_subject.delete()
            return JsonResponse({"success" : True, "subject" : subject}, status = 200)
        error = form.errors.get_json_data()   
        return JsonResponse(error, status = 404)

class UniversityScoreListView(ScoreListView):
    """
        GET all scores of particular Subject sorted by University
    """

    def get_scores(self, request):
        universities = University.objects.filter(
            rank__gt = 0
            ).prefetch_related(
                Prefetch(
                    "scores_by_category",
                    queryset=UniversityScoreByCategory.objects.order_by(
                            "-criterion_category__university_only",
                            "criterion_category_id"
                            ).select_related(
                                'criterion_category'
                            ).prefetch_related(
                                Prefetch('cri_scores', queryset=UniversityScore.objects.select_related('criterion'))
                            )   
                )
            )
        result = []
        for university in universities:
            university_id = university.id
            university_name = university.name
            university_href = university.get_absolute_url()
            scores_by_category = university.scores_by_category.all()
            scores = []
            for score_by_category in scores_by_category:
                data = get_all_scores_from_category_score(score_by_category, labeled=False)
                scores.append(data)
            result.append({"university" : {"id" : university_id, "university" : university_name, "href" : university_href}, "scores" : scores})
        return JsonResponse(result, safe=False)

    
class UniversityScoreDetailView(ScoreDetailView):
    """
         Manage to change/delete based on university's score 
         Model UniversityScore
    """

    error_messages = {
        "category" : [
            {"code" : "invalid", "message" : "This category is invalid"},
        ],
        "university" : [
            {"code" : "invalid", "message" : "This university is invalid"}
        ]
    
    }

    def get_scores(self, request, university_id):
        try: 
            university = University.objects.get(id = university_id)
        except University.DoesNotExist:
            field = "university"
            return json_error(field, self.error_messages)
        else:
            filter = request.GET.get("filter")
            labeled = string_to_boolean(request.GET.get("label"))
            result = {}
            if filter == self.ScoresFiltering.ONLY_CATEGORY_SCORES:
                result['categoryScores'] = get_category_scores_of_object(university, labeled)
            elif filter == self.ScoresFiltering.ONLY_CRITERION_SCORES:
                #not implemented yet
                result = {"scores" : []}
            else:
                #filter == self.ScoresFiltering.ALL_SCORES
                result["score"] = get_scores_of_object(university, labeled)
            result["subject"] = "Toàn Trường"
            result["university_id"] = university_id
            return JsonResponse(result)
            
    
    @method_decorator(permission_required_or_403("university.change_university", (University, 'id', 'university_id')))
    def add_score(self, request, university_id):
        request_data = request.POST
        input = {"university" : university_id, "criterion" : request_data.get("criterion"), "score" : request_data.get("score")}
        score_form = UniversityScoreAddForm(input)
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
        score_form = UniversityScoreEditForm(input)
        if score_form.is_valid():
            score_form.save()
            return JsonResponse({"success" : True})
        else:
            error = score_form.errors.get_json_data()   
            return JsonResponse(error)

    @method_decorator(permission_required_or_403("university.change_university", (University, 'id', 'university_id')))
    def delete_score(self, request, university_id):
        request_data = request.DELETE
        input = {"university" : university_id, "criterion" : request_data.get("criterion"), "score" : 0}
        delete_form = UniversityScoreDeleteForm(input)
        if delete_form.is_valid():
            delete_form.delete_object()
            return JsonResponse({"success" : True}, status = 200)
        else:
            error = delete_form.errors.get_json_data()   
            return JsonResponse(error)