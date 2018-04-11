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

