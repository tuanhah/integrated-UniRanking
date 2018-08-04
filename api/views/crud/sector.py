from django.http import JsonResponse
from user.forms import AddSectorForm, UpdateSectorForm, RemoveSectorForm
from subject.models import Sector, UniversitySector

def add_sector(request):
    form = AddSectorForm(request.POST)
    all_sector = Sector.objects.all()
    sectors_name = []
    for sector in all_sector:
        sectors_name.append(sector.name)

    if request.method == "POST":
        if form.is_valid():
            new_sector_name = form.cleaned_data['name']
            if new_sector_name not in sectors_name:
                form.save()
                return JsonResponse({'success' : True, "name": new_sector_name})
            else:
                return JsonResponse({'success' : False, 'code' : 'already'})
    # errors = form.errors.get_json_data()
    errors = {'success' : False, 'code' : "failed"}
    return JsonResponse(errors)

def update_sector(request):
    form = AddSectorForm(request.POST)
    all_sector = Sector.objects.all()
    sectors_name = []
    for sector in all_sector:
        sectors_name.append(sector.name)

    if request.method == "POST":
        if form.is_valid():
            update_sector_id = request.POST['sector_id']
            update_sector_name = form.cleaned_data['name']
            if update_sector_name not in sectors_name:
                try:
                    sector = Sector.objects.get(pk=update_sector_id)
                except Sector.DoesNotExist:
                    return JsonResponse({"success" : False, "code": "doesnotexist"})
                else:
                    old_sector_name = sector.name;
                    sector.name = update_sector_name
                    sector.save()
                    return JsonResponse({'success' : True, "old": old_sector_name, "new": update_sector_name})
            else:
                return JsonResponse({'success' : False, 'code' : 'already'})
    errors = {'success': False, 'code': "failed"}
    return JsonResponse(errors)
def remove_sector(request):
    form = RemoveSectorForm(request.POST)
    all_sector = Sector.objects.all()
    sectors_name = []
    for sector in all_sector:
        sectors_name.append(sector.name)

    if request.method == "POST":
        if form.is_valid():
            delete_sectors_id = request.POST['sector_id']
            try:
                sector = Sector.objects.get(pk=delete_sectors_id)
            except Sector.DoesNotExist:
                return JsonResponse({"success": False, "code": "doesnotexist"})
            else:
                name = sector.name
                sector.delete()
                return JsonResponse({'success': True, 'name': name})
    return JsonResponse({'success': False, 'code': 'failed'})
