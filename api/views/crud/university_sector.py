from django.http import JsonResponse
from user.forms import AddUniversitySectorForm, RemoveUniversitySectorForm
from subject.models import Sector, UniversitySector
from university.models import University

def add_university_sector(request):
    form = AddUniversitySectorForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            university_id = request.POST['university']
            sector_id = request.POST['sector']
            university_sector = form.save(commit=False)
            try:
                university = University.objects.get(pk=university_id)
                sector = Sector.objects.get(pk=sector_id)
            except University.DoesNotExist:
                return JsonResponse({"success": False, "code": "universitydoesnotexist"})
            except Sector.DoesNotExist:
                return JsonResponse({"success": False, "code": "sectordoesnotexist"})
            else:
                university_sector.university = university
                university_sector.sector = sector
                university_sector.save()
                return JsonResponse({'success' : True, 'university' : university.name, 'sector' : sector.name})
    # errors = form.errors.get_json_data()
    errors = {'success' : False, 'code' : "failed"}
    return JsonResponse(errors)


def remove_university_sector(request):
    pass