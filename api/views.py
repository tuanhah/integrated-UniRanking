from collections import OrderedDict
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from UniRanking.forms import UserRegistrationForm
from university.models import University, UniversitySubject
from university.forms import UniversitySubjectDeleteForm, UniversitySubjectCreateForm, UniversityScoreForm, UniversityScoreEditForm, UniversityScoreDeleteForm
from subject.forms import SubjectScoreForm, SubjectScoreEditForm, SubjectScoreDeleteForm
from subject.models import GroupSubject, Subject
from university.forms import U_EDITABLE_CATEGORY_LIST
from criteria.models import CategoryCriterion, Criterion

def login(request):
    form = AuthenticationForm(None, request.POST)
    if request.method == "POST" and request.user.is_anonymous:
        if form.is_valid():
            auth(request, form.get_user())
            return JsonResponse({'success' : True})
    errors = form.errors.get_json_data()   
    return JsonResponse(errors)

def register(request):
    form = UserRegistrationForm(request.POST)
    if request.method == "POST" and request.user.is_anonymous:
        if form.is_valid():
            form.save()
            return JsonResponse({'success' : True})
    errors = form.errors.get_json_data()   
    return JsonResponse(errors)

def get_subjects(request):
    if request.method == "POST":
        univ_id = request.POST['university']
        university = University.objects.get(id = univ_id)
        name = university.name
        editable = True
        sorted_subjects = get_sorted_subjects(university)
        result = {"name" : name, "editable" : editable, "subjects" : sorted_subjects}
        return JsonResponse(result)    


def get_sorted_subjects(university):
    from itertools import groupby
    result = OrderedDict()
    sorted_subjects = university.subjects.order_by("group")        
    sorted_subjects = sorted(sorted_subjects, key = lambda s : s.root_group())
    iter = groupby(sorted_subjects, key = lambda s : s.root_group())
    for root_group, subjects in iter:
        result[root_group] = OrderedDict()
        inner_iter = groupby(subjects, key = lambda s : s.group)
        for group, inner_subjects in inner_iter:
            group_name = group.name
            if group_name == root_group:
                group_name = "Khác"
            current_group = result[root_group][group_name] = OrderedDict()
            for subject in inner_subjects:
                current_group[subject.name] = subject.id
    return result

def get_scores(request):
    if request.method == "POST":
        university_id = request.POST["university"]
        if 'subject' in request.POST:
            subject_id = request.POST['subject'] 
            univ_subject = get_object_or_404(UniversitySubject, university_id = university_id, subject_id = subject_id )
            name = univ_subject.subject.name
            scores = get_scores_of_object(univ_subject)
            result = {"name" : name, "scores" : scores}
        else:
            university = get_object_or_404(University, id = university_id)
            scores = get_scores_of_object(university)
            result = {"name" : "Toàn Trường", "scores" : scores}
        return JsonResponse(result)

def get_scores_of_object(_object):
    result = OrderedDict()
    scores_by_category = _object.scores_by_category.order_by("category_criterion")
    for score_by_category in scores_by_category:
        category = score_by_category.category_criterion
        category_id = category.id
        category_name = category.name
        score = round(score_by_category.score, 2)
        result[category_name] = {"id" : category_id, "score" : score, "detail" : []}
        cri_scores = score_by_category.cri_scores.all()
        for cri_score in cri_scores:
            criterion = cri_score.criterion
            cri_id = criterion.id
            cri_name = criterion.name
            cri_descr = criterion.description
            score = round(cri_score.score,2)
            detail = { "id" : cri_id, "name" : cri_name, "description" : cri_descr, "score" : score}
            result[category_name]["detail"].append(detail)
    return result

def delete_subject(request):
    form = UniversitySubjectDeleteForm(request.POST or None)
    if form.is_valid():
        univ_subject = form.get_univ_subject_object()
        subject = univ_subject.subject.name
        univ_subject.delete()
        return JsonResponse({"success" : True, "subject" : subject})
    error = form.errors.get_json_data()   
    return JsonResponse(error)
    
def add_subject(request):
    form = UniversitySubjectCreateForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit = False)
        subject = instance.subject.name
        instance.save() 
        return JsonResponse({"success" : True, "subject" : subject})
    error = form.errors.get_json_data()   
    return JsonResponse(error)

def get_groups_of_sector(request):
    error_messages = {
        "sector" : [
            {"code" : "invalid", "message" : "This sector is invalid"},
            {"code" : "required", "message" : "Sector field is required"},
        ]
    }

    if request.method == "POST":
        field = "sector"
        if 'sector' in request.POST:
            sector_id = request.POST['sector']
            try:
                sector = GroupSubject.objects.get(id = sector_id)
            except GroupSubject.DoesNotExist:
                error = error_messages[field][0]
                return JsonResponse({field : {"code" : error["code"], "message" : error["message"]}})
            else:
                if sector.parent is not None: 
                    error = error_messages[field][0]
                    return JsonResponse({field : {"code" : error["code"], "message" : error["message"]}})
                else:
                    groups_queryset = sector.groups.all()
                    list_group = [{"id" : group.id, "name" : group.name} for group in groups_queryset]
                    result = {"success" : True, "groups" : list_group}
                    return JsonResponse(result)
        else:
            error = error_messages[field][1]
            return JsonResponse({field : {"code" : error["code"], "message" : error["message"]}})
    return JsonResponse({})

def get_subjects_of_group(request):
    error_messages = {
        "group" : [
            {"code" : "invalid", "message" : "This group is invalid"},
            {"code" : "required", "message" : "Group field is required"},
        ],
        "university" : [
            {"code" : "invalid", "message" : "This university is invalid"},
            {"code" : "required", "message" : "University field is required"},
        ],
    }

    if request.method == "POST":
        field = "group"
        if 'group' in request.POST and 'university' in request.POST:
            #exception here
            university_id = request.POST['university']
            university = University.objects.get(id = university_id)

            group_id = request.POST['group']
            try:
                group = GroupSubject.objects.get(id = group_id)
            except GroupSubject.DoesNotExist:
                error = error_messages[field][0]
                return JsonResponse({field : {"code" : error["code"], "message" : error["message"]}})
            else:
                if group.parent is None: 
                    error = error_messages[field][0]
                    return JsonResponse({field : {"code" : error["code"], "message" : error["message"]}})
                else:
                    subjects_of_univ_queryset = university.subjects.filter(group = group)
                    subjects_non_added_queryset = group.subjects.exclude(pk__in = subjects_of_univ_queryset)
                    list_subject_added = [{"id" : subject.id, "name" : subject.name, 'added' : True} for subject in subjects_of_univ_queryset]
                    list_subject_non_added = [{"id" : subject.id, "name" : subject.name} for subject in subjects_non_added_queryset]
                    list_subject = list_subject_added + list_subject_non_added
                    result = {"success" : True, "subjects" : list_subject}
                    return JsonResponse(result)
        else:
            error = error_messages[field][1]
            return JsonResponse({field : {"code" : error["code"], "message" : error["message"]}})
    return JsonResponse({})

def edit_score(request):
    if request.method == "POST" and 'target' in request.POST:
        request_data = request.POST
        target = request_data.get("target")
        if target == "subject": #edit univ_subject score
            UniversitySubjectCheckExistForm = UniversitySubjectDeleteForm # get university_id and subject_id from request and use clean() for validating =>>> univ_subject
            check_exist_form = UniversitySubjectCheckExistForm(request_data)
            if check_exist_form.is_valid():
                univ_subject = check_exist_form.get_univ_subject_object()
                input = {"univ_subject" : univ_subject.pk, "criterion" : request_data.get("criterion"), "score" : request_data.get("score")}
                score_form = SubjectScoreEditForm(input)
                if score_form.is_valid():
                    score_form.save()
                    return JsonResponse({"success" : "True"})
                else:
                    error = score_form.errors.get_json_data()   
                    return JsonResponse(error)
            else:
                error = check_exist_form.errors.get_json_data()   
                return JsonResponse(error)
        elif target == 'university': #edit university_score
            score_form = UniversityScoreEditForm(request_data)
            if score_form.is_valid():
                score_form.save()
                return JsonResponse({"success" : True})
            else:
                error = score_form.errors.get_json_data()   
                return JsonResponse(error)
    return JsonResponse({})

def get_editable_criterion_categories(request):
    if request.method == "POST" and 'target' in request.POST:
        request_data = request.POST
        target = request_data.get("target")
        if target == "subject":
            categories_queryset = CategoryCriterion.objects.exclude(pk__in = [category[0] for category in U_EDITABLE_CATEGORY_LIST])
        elif target == 'university':
           categories_queryset = CategoryCriterion.objects.filter(pk__in = [category[0] for category in U_EDITABLE_CATEGORY_LIST])
        categories = [{"id" : category.id, "name" : category.name} for category in categories_queryset.all()]
        return JsonResponse({"success" : True, "categories" : categories})
    return JsonResponse({})


def get_criteria_of_category(request):
    if request.method == "POST" and 'target' in request.POST:
        request_data = request.POST
        target = request_data.get("target")
        if target == "subject": #get add & non-add criteria of univ_subject
            UniversitySubjectCheckExistForm = UniversitySubjectDeleteForm
            check_exist_form = UniversitySubjectCheckExistForm(request_data)
            if check_exist_form.is_valid():
                univ_subject = check_exist_form.get_univ_subject_object()
                input = {"univ_subject" : univ_subject.pk, "criterion" : 4, "score" : 0} #criterion is randomed from editable_list
                score_form = SubjectScoreForm(input)
                if score_form.is_valid():
                    category = request_data.get("category")
                    added_criterion_scores, non_added_criterion_scores = score_form.get_criterion_scores_of_category(category)
                    return JsonResponse({"success" : "True", "added_criterion_scores" : added_criterion_scores, "non_added_criterion_scores" : non_added_criterion_scores})
                else:
                    error = score_form.errors.get_json_data()   
                    return JsonResponse(error)
            else:
                error = check_exist_form.errors.get_json_data()   
                return JsonResponse(error)
        elif target == 'university':
            input = {"university" : request_data.get("university"), "criterion" : 1, "score" : 0}
            score_form = UniversityScoreForm(input)
            if score_form.is_valid():
                category = request_data.get("category")
                added_criterion_scores, non_added_criterion_scores = score_form.get_criterion_scores_of_category(category)
                return JsonResponse({"success" : "True", "added_criterion_scores" : added_criterion_scores, "non_added_criterion_scores" : non_added_criterion_scores})
            else:
                error = score_form.errors.get_json_data()   
                return JsonResponse(error)
    return JsonResponse({})

def delete_score(request):
    request_data = request.POST
    if 'subject' in request_data: 
        UniversitySubjectCheckExistForm = UniversitySubjectDeleteForm 
        check_exist_form = UniversitySubjectCheckExistForm(request_data or None)
        if check_exist_form.is_valid():
            univ_subject = check_exist_form.get_univ_subject_object()
            input = {"univ_subject" : univ_subject.pk, "criterion" : request_data.get("criterion"), "score" : 0}
            delete_form = SubjectScoreDeleteForm(input)
            if delete_form.is_valid():
                subject_score = delete_form.get_subject_score_object()
                subject_score.delete()
                return JsonResponse({"success" : True})
            error = delete_form.errors.get_json_data()   
            return JsonResponse(error)
        error = check_exist_form.errors.get_json_data()   
        return JsonResponse(error)
    else:
        input = {"university" : request_data.get("university"), "criterion" : request_data.get("criterion"), "score" : 0}
        delete_form = UniversityScoreDeleteForm(input)
        if delete_form.is_valid():
            univ_score = delete_form.get_univ_score_object()
            univ_score.delete()
            return JsonResponse({"success" : True})
        else:
            error = delete_form.errors.get_json_data()   
            return JsonResponse(error)
    return JsonResponse(error)