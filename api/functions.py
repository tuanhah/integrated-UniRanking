from itertools import groupby
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

def string_to_boolean(value):
    if value is not None and value.lower() == 'false':
        return False
    else:
        return True

def get_sorted_univ_subjects(university):
    result = []
    sorted_subjects = university.subjects.select_related("group__parent")        
    sorted_subjects = sorted(sorted_subjects, key = lambda s : s.sector().id)
    iter = groupby(sorted_subjects, key = lambda s : s.sector())
    for sector, subjects in iter:
        inner_iter = groupby(subjects, key = lambda s : s.group)
        group_list = []
        for group, inner_subjects in inner_iter:
            subject_list = []
            for subject in inner_subjects:
                subject_list.append({"id" : subject.id,"name" : subject.name})
            group_list.append({"group": {"id": group.id , "name" : group.name}, "subjects" : subject_list})
        result.append({"sector" : {"id" : sector.id, "name" : sector.name} , "groups" : group_list})
    return result

def get_all_subjects_of_group(university, group):
    subjects_of_univ_queryset = university.subjects.filter(group = group)
    subjects_non_added_queryset = group.subjects.exclude(pk__in = subjects_of_univ_queryset)
    list_subject_added = [{"id" : subject.id, "name" : subject.name, 'added' : True} for subject in subjects_of_univ_queryset]
    list_subject_non_added = [{"id" : subject.id, "name" : subject.name} for subject in subjects_non_added_queryset]    
    list_subject = list_subject_added + list_subject_non_added
    return list_subject

def get_score_model(_object):
    if isinstance(_object, University):
        score_model = UniversityScore
    else:  #Subject model
        score_model = SubjectScore
    return score_model 

def parse_category_score(category_score, labeled=True):
    result = {}
    if labeled:
        category = category_score.criterion_category
        category_id = category.id
        category_name = category.name
        result = {"id" : category_id, "name" : category_name}
    else:
        category_id = category_score.criterion_category_id
        result = {"id" : category_id}
    result['score'] = category_score.score
    return result

def parse_criterion_score(criterion_score, labeled = True):
    result = {}
    if labeled:
        criterion = criterion_score.criterion
        cri_id = criterion.id
        cri_name = criterion.name
        cri_description = criterion.description
        result = {"id": cri_id, "name": cri_name, "description": cri_description}
    else:
        cri_id = criterion_score.criterion_category_id
        result = {"id": cri_id}
    result['score'] = criterion_score.score
    return result


def get_all_scores_from_category_score(category_score, labeled = "True"):
    result = {}
    result["categoryScore"] = parse_category_score(category_score, labeled)
    cri_scores = category_score.cri_scores.all()
    detail = []
    for cri_score in cri_scores:
        parse_cri_score = parse_criterion_score(cri_score, labeled)
        detail.append(parse_cri_score)
    result['criterionScores'] = detail
    return result

def get_scores_of_object(_object, labeled = True):        
    result = []
    if labeled:
        score_model = get_score_model(_object)
        category_scores = _object.scores_by_category.order_by(
                "-criterion_category__university_only",
                "criterion_category_id"
            ).select_related(
                'criterion_category'
            ).prefetch_related(
                Prefetch('cri_scores', queryset=score_model.objects.select_related('criterion'))
            )
    else:
        category_score = _object.scores_by_category.order_by(
                "-criterion_category__university_only",
                "criterion_category_id"
            ).prefetch_related(
                'cri_scores'
            )

    for category_score in category_scores:
        data = get_all_scores_from_category_score(category_score, labeled)
        result.append(data)
    return result

def get_category_scores_of_object(_object, labeled):
    result = []
    if labeled:
        category_scores = _object.scores_by_category.order_by(
            "-criterion_category__university_only",
            "criterion_category_id"
            ).select_realted(
                'criterion_category'
            )
    else:
        catgory_scores = _object.scores_by_category.order_by(
            "criterion_category_id"
            )
    for category_score in category_scores:
        parsed_score = parse_category_score(category_score, labeled)
        result.append(parsed_score)
    return result