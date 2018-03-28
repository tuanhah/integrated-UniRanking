from django.http import JsonResponse
from django.contrib.auth import login as auth
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from UniRanking.forms import UserRegistrationForm


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



def get_university(request):
    if request.method == "POST":
        university =[{"id": uni.id, "name": uni.name } for uni in University.objects.all()]
        result = {"success": True, "universities" : university}
        return JsonResponse(result)
def get_all_sector(request):
    if request.method == "POST":
        
        sector = [{"id": st.id, "name": st.name} for st in GroupSubject.objects.filter(parent_id__isnull=True)]
        result = {"success": True, "sectors": sector} 
        return JsonResponse(result)
def get_all_group_subject(request):
    if request.method == "POST":
        groupsubject = []
        for gs in GroupSubject.objects.all():
            if gs.parent_id is not None:
                groupsubject.append({"id": gs.id, "parent_id": gs.parent_id, "name": gs.name})
        result = {"success": True, "GroupSubject": groupsubject}
        return JsonResponse(result)
def get_all_subject_of_group(request):
    error_messages = {
        "group" : [
            {"code" : "invalid", "message" : "This group is invalid"},
            {"code" : "required", "message" : "Group field is required"},
        ],
    }

    if request.method == "POST":
        field = "group"
        if 'group' in request.POST:
            #exception here
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
                    subjects_queryset = group.subjects.all()
                    list_subject = [{"id" : subject.id, "name" : subject.name, 'added' : True} for subject in subjects_queryset]
                    result = {"success" : True, "subjects" : list_subject}
                    return JsonResponse(result)
        else:
            error = error_messages[field][1]
            return JsonResponse({field : {"code" : error["code"], "message" : error["message"]}})
    return JsonResponse({})
def get_subject_from_id(request):
    error_messages = {
        "id" : [
            {"code" : "invalid", "message" : "This id is invalid"},
            {"code" : "required", "message" : "Id is required"},
        ],
    }
    if request.method == "POST":
        field = "id"
        if 'id' in request.POST:
            subject_id = request.POST['id']
            try:
                subject = Subject.objects.get(id = subject_id)
            except Subject.DoesNotExist:
                error = error_messages[field][0]
                return JsonResponse({field : {"code": error["code"], "message" : error["message"]}})
            else:
                sub = [{"id" : subject.id, "name": subject.name}]
                result = {"success": True, "subject": sub}
                return JsonResponse(result)
        else:
            error = error_messages[field][1]
            return JsonResponse({field : {"code" : error["code"], "message" : error["message"]}})
    return JsonResponse({})
def get_all_criterions_of_category_university(request):
    error_messages = {
        "id": [
            {"code": "invalid", "message": "This id is invalid"},
            {"code": "required", "message": "This id is required"},
        ],
         
    }
    if request.method == "POST":
        field = "id"
        if 'id' in request.POST:
            category_id = request.POST['id']
            try:
                category = CategoryCriterion.objects.get(id = category_id)
            except CategoryCriterion.DoesNotExist:
                error = error_messages[field][0]
                return JsonResponse({field : {"code": error["code"], "message": error["message"]}})
            else:
                criterion = [{"id" : crit.id, "name": crit.name} for crit in Criterion.objects.filter(category_id = category_id)]
                result = {"success": True, "criterions": criterion}
                return JsonResponse(result)
        else:
            error = error_messages[field][1]
            return JsonResponse({field : {"code": error["code"], "message": error["message"]}})
    return JsonResponse({})
