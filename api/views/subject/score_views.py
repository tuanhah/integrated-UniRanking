from django.http import JsonResponse
from django.utils.decorators import method_decorator
from guardian.decorators import permission_required_or_403

from university.models import University
from subject.models import UniversitySubject
# from subject.forms import SubjectScoreByCriterionCreateForm, SubjectScoreByCriterionEditForm
from api.views.base import BaseManageView, RankingView, ScoreDetailView
from api.functions import string_to_boolean

# class SubjectRankingView(RankingView):
#     """
#         GET University ranking of particular Subject
#     """

#     def get_ranking(self, request, subject_id):
#         univ_subjects = UniversitySubject.objects.filter(
#                 subject_id = subject_id
#             ).select_related(
#                 "university",
#                 "subject"
#             ).order_by_rank().prefetch_scores()
#         result = {"rank" : [univ_subject.parse_data() for univ_subject in univ_subjects]}
#         return JsonResponse(result)

# class SubjectScoreDetailView(ScoreDetailView):
#     """
#         Manage to change/delete based on each subject's score of university
#         Model SubjectScore (UniversitySubjectScore)
#     """

#     error_messages = {
#         "category" : {
#             "invalid" : "This category is invalid",
#         },
#         "__all__" : {
#             "invalid" : "This university or subject is invalid",
#         }
#     }

#     def get_scores(self, request, university_id, subject_id):
#         univ_subject_queryset = UniversitySubject.objects.select_related(
#                 "university",
#                 "subject"
#             ).filter(
#                 university_id = university_id,
#                 subject_id = subject_id
#             )        
#         filter = request.GET.get("filter")
#         named = string_to_boolean(request.GET.get("named"))
#         result = {}
#         if filter == self.ScoresFiltering.ONLY_CATEGORY_SCORES:
#             univ_subject = univ_subject_queryset.prefetch_criterion_category_scores().first()
#             if univ_subject is None: 
#                 return self.json_error(field = '__all__', code = "invalid")
#             else:            
#                 result["criterion_category_scores"] = univ_subject.parse_criterion_category_scores(named = named)
#         elif filter == self.ScoresFiltering.ONLY_CRITERION_SCORES:
#             result = {"scores" : []} #not implemented yet
#         else:
#             #filter == self.ScoresFiltering.ALL_SCORES(default)
#             univ_subject = univ_subject_queryset.prefetch_scores().first()
#             if univ_subject is None: 
#                 return self.json_error(field = '__all__', code = "invalid")
#             else:            
#                 result["scores"] = univ_subject.parse_scores(named = named)
#         univ_subject_info = univ_subject.parse_basic_info()
#         result["profile"] = univ_subject_info
#         return JsonResponse(result)

#     @method_decorator(permission_required_or_403("university.change_university", (University, 'id', 'university_id')))
#     def add_score(self, request, university_id, subject_id):
#         try: 
#             univ_subject = UniversitySubject.objects.get(university = university_id, subject = subject_id)
#         except UniversitySubject.DoesNotExist:
#             return self.json_error(field = '__all__', code = "invalid")
#         else:
#             request_data = request.POST
#             input = {"univ_subject" : univ_subject.pk, "criterion" : request_data.get("criterion"), "score" : request_data.get("score")}
#             score_form = SubjectScoreByCriterionCreateForm(input)
#             if score_form.is_valid():
#                 score_form.save()
#                 return JsonResponse({"success" : "True"}, status = 201)
#             else:
#                 error = score_form.errors.get_json_data()   
#                 return JsonResponse(error, status = 404)


#     @method_decorator(permission_required_or_403("university.change_university", (University, 'id', 'university_id')))
#     def edit_score(self, request, university_id, subject_id):
#         try: 
#             univ_subject = UniversitySubject.objects.get(university = university_id, subject = subject_id)
#         except UniversitySubject.DoesNotExist:
#             return self.json_error(field = '__all__', code = "invalid")
#         else:
#             request_data = request.PUT
#             input = {"univ_subject" : univ_subject.pk, "criterion" : request_data.get("criterion"), "score" : request_data.get("score")}
#             score_edit_form = SubjectScoreByCriterionEditForm(input)
#             if score_edit_form.is_valid():
#                 score_edit_form.save()
#                 return JsonResponse({"success" : "True"})
#             else:
#                 error = score_edit_form.errors.get_json_data()   
#                 return JsonResponse(error, status = 404)

#     @method_decorator(permission_required_or_403("university.change_university", (University, 'id', 'university_id')))
#     def delete_score(self, request, university_id, subject_id):
#         try: 
#             univ_subject = UniversitySubject.objects.get(university = university_id, subject = subject_id)
#         except UniversitySubject.DoesNotExist:
#             return self.json_error(field = '__all__', code = "invalid")
#         else:
#             request_data = request.POST
#             input = {"univ_subject" : univ_subject.pk, "criterion" : request_data.get("criterion"), "score" : 0}
#             delete_form = SubjectScoreByCriterionEditForm(input)
#             if delete_form.is_valid():
#                 delete_form.delete()
#                 return JsonResponse({"success" : True}, status = 200)
#             else:
#                 error = delete_form.errors.get_json_data()   
#                 return JsonResponse(error)