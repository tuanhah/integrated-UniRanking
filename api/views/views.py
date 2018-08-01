from django.http import JsonResponse
from django.contrib.auth import login as auth, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from UniRanking.forms import UserRegistrationForm, SectorForm
from subject.models import Sector, UniversitySector



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
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            auth(request, new_user)
            return JsonResponse({'success' : True})
    errors = form.errors.get_json_data()   
    return JsonResponse(errors)

def add_sector(request):
    form = SectorForm(request.POST)
    all_sector = Sector.objects.all()
    sectors_name = []
    for sector in all_sector:
        sectors_name.append(sector.name)

    if request.method == "POST":
        if form.is_valid():
            new_sector_name = form.cleaned_data['name']
            if new_sector_name not in sectors_name:
                form.save()
                return JsonResponse({'success' : True, "message": "Add successfully!"})
            else:
                return JsonResponse({'success' : False, 'message' : 'This item have already been in database'})
    # errors = form.errors.get_json_data()
    errors = {'success' : False, 'message' : "Can't add this Sector"}
    return JsonResponse(errors)
