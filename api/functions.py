from django.http import JsonResponse
from django.db.models import Prefetch
from university.models import University, UniversityScore
from subject.models import SubjectScore

def json_error(field, error_messages, error_indices = (0,)):
    field_errors = []
    for index in error_indices:
        error = error_messages[field][index]
        field_errors.append({"code" : error["code"], "message" : error["message"]})
    return JsonResponse({field : field_errors}, safe = False, status = 404)

def get_sorted_univ_subjects(university):
    from itertools import groupby
    result = []
    sorted_subjects = university.subjects.select_related("group", "group__parent").order_by("group")        
    sorted_subjects = sorted(sorted_subjects, key = lambda s : s.sector())
    iter = groupby(sorted_subjects, key = lambda s : s.sector())
    for sector, subjects in iter:
        inner_iter = groupby(subjects, key = lambda s : s.group)
        group_list = []
        for group, inner_subjects in inner_iter:
            group_name = group.name
            if group_name == sector:
                group_name = "Khác"
            subject_list = []
            for subject in inner_subjects:
                subject_list.append({"id" : subject.id,"name" : subject.name})
            group_list.append({"name" : group_name, "subjects" : subject_list})
        result.append({"name" : sector , "groups" : group_list})
    return result

def get_all_subjects_of_group(university, group):
    subjects_of_univ_queryset = university.subjects.filter(group = group)
    subjects_non_added_queryset = group.subjects.exclude(pk__in = subjects_of_univ_queryset)
    list_subject_added = [{"id" : subject.id, "name" : subject.name, 'added' : True} for subject in subjects_of_univ_queryset]
    list_subject_non_added = [{"id" : subject.id, "name" : subject.name} for subject in subjects_non_added_queryset]    
    list_subject = list_subject_added + list_subject_non_added
    return list_subject


def get_all_scores_from_category_score(score_by_category):
    category = score_by_category.criterion_category
    category_id = category.id
    category_name = category.name
    score = score_by_category.score
    cri_scores = score_by_category.cri_scores.all()
    detail = []
    for cri_score in cri_scores:
        criterion = cri_score.criterion
        cri_id = criterion.id
        cri_name = criterion.name
        cri_descr = criterion.description
        score = cri_score.score
        detail.append({ "id" : cri_id, "name" : cri_name, "description" : cri_descr, "score" : score})
    result = {"id" : category_id, "name" : category_name, "score" : score, "detail" : detail}
    return result

def get_scores_of_object(_object):
    result = []
    #check type of object for choosing appropriate score model
    if isinstance(_object, University):
        score_model = UniversityScore
    else:
        score_model = SubjectScore
    
    scores_by_category = _object.scores_by_category.order_by(
        "-criterion_category__university_only",
        "criterion_category_id"
        ).select_related(
            'criterion_category'
        ).prefetch_related(
            Prefetch('cri_scores', queryset=score_model.objects.select_related('criterion'))
        )
    
    for score_by_category in scores_by_category:
        data = get_all_scores_from_category_score(score_by_category)
        result.append(data)
    return result

def get_category_scores_of_object(_object):
    result = []
    scores_by_category = _object.scores_by_category.order_by(
        "criterion_category_id"
        ).select_related(
            'criterion_category'
        )
    
    for score_by_category in scores_by_category:
        category = score_by_category.criterion_category
        category_id = category.id
        category_name = category.name
        score = score_by_category.score
        result.append({"id" : category_id, "name" : category_name, "score" : score})
    return result