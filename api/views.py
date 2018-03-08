from collections import OrderedDict
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from UniRanking.forms import UserRegistrationForm
from university.models import University, UniversitySubject

def login(request):
    form = AuthenticationForm(None, request.POST or None)
    if request.method == "POST" and request.user.is_anonymous:
        if form.is_valid():
            auth(request, form.get_user())
            return JsonResponse({'success' : True})
    error = form.errors.get_json_data()   
    error.update({"success" : False}) 
    return JsonResponse(error)

def register(request):
    form = UserRegistrationForm(request.POST or None)
    if request.method == "POST" and request.user.is_anonymous:
        if form.is_valid():
            form.save()
            return JsonResponse({'success' : True})
    error = form.errors.get_json_data()   
    return JsonResponse(error)

def get_scores(request):
    if request.method == "POST":
        university_id = request.POST["university"]
        if 'subject' in request.POST:
            subject_id = request.POST['subject'] 
            univ_subject = get_object_or_404(UniversitySubject, university_id = university_id, subject_id = subject_id )
            return get_scores_by_subject(univ_subject)
        else:
            university = get_object_or_404(University, id = university_id)
            return get_scores_by_university(university)

def get_scores_by_subject(univ_subject):
    response = OrderedDict()
    response["success"] = False
    scores_by_category = univ_subject.scores_by_category.order_by("category_criterion")
    for score_by_category in scores_by_category:
        category = score_by_category.category_criterion.name
        score = score_by_category.score
        response[category] = {"score" : score, "detail" : []}
        cri_scores = score_by_category.cri_scores.all()
        for cri_score in cri_scores:
            criterion = cri_score.criterion
            cri_name = criterion.name
            cri_descr = criterion.description
            score = cri_score.score
            detail = { "name" : cri_name, "description" : cri_descr, "score" : score}
            response[category]["detail"].append(detail)
    response["success"] = True
    print(response)
    return JsonResponse(response)

def get_scores_by_university(university):
    response = OrderedDict()
    response["success"] = False
    scores_by_category = university.scores_by_category.order_by("category_criterion")
    for score_by_category in scores_by_category:
        category = score_by_category.category_criterion.name
        score = score_by_category.score
        response[category] = {"score" : score, "detail" : []}
        cri_scores = score_by_category.cri_scores.all()
        for cri_score in cri_scores:
            criterion = cri_score.criterion
            cri_name = criterion.name
            cri_descr = criterion.description
            score = cri_score.score
            detail = { "name" : cri_name, "description" : cri_descr, "score" : score}
            response[category]["detail"].append(detail)
    response["success"] = True
    print(response)
    return JsonResponse(response)