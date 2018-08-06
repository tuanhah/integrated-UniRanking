from django.http import JsonResponse
from user.forms import AddFavouriteUniversityForm, RemoveFavouriteUniversityForm
from django.contrib.auth.models import User
from university.models import University, UserFavouriteUniversity

def add_favourite_university(request):
    form = AddFavouriteUniversityForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            user_university = form.save(commit=False)
            user = request.user
            university_id = request.POST['university']
            university = University.objects.get(pk=university_id)
            user_university.user = user
            user_university.university = university
            user_university.save()
            return JsonResponse({'success': True, "name": university.name})
    errors = {'success': False, 'code': "failed"}
    return JsonResponse(errors)

def remove_favourite_university(request):
    form = RemoveFavouriteUniversityForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            user = request.user
            university_id = request.POST['university']
            university = University.objects.get(pk=university_id)
            user_university = UserFavouriteUniversity.objects.filter(user = user, university = university)
            user_university.delete()
            return JsonResponse({'success': True, "name": university.name})
    errors = {'success': False, 'code': "failed"}
    return JsonResponse(errors)